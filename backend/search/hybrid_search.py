import re
from dataclasses import dataclass
from search.dense_search import Retrieved_chunks , embedd_query
from sqlalchemy import select , text
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import Knowledge_base

@dataclass
class Hybrid_chunks(Retrieved_chunks):
    dense_rank: int | None = None
    keyword_rank: int | None = None


token_re = re.compile(r"[A-Za-z0-9]+")

def build_query_ts(query):
    tokens = {t.lower() for t in token_re.findall(query) if len(t) > 1}
    return " | ".join(sorted(tokens)) if tokens else None

async def keyword_search(db: AsyncSession , query: str , k : int = 5):
    tsquery = build_query_ts(query)
    if not tsquery:
        return []
    db_query =  text("SELECT id FROM knowledge_chunks WHERE chunks_tsv @@ to_tsquery('english', :q) ORDER BY ts_rank(chunks_tsv, to_tsquery('english', :q)) DESC LIMIT :k")   
    rows = (await db.execute(db_query , {"q": tsquery , "k": k})).all()
    return [str(r.id) for r in rows]

async def dense_search(db : AsyncSession , query: str , k:int = 5):
    query_vec = await embedd_query(query)
    distance = Knowledge_base.embedding.cosine_distance(query_vec)
    db_query = select(Knowledge_base.id).order_by(distance).limit(k)
    return [str(i) for i in (await db.execute(db_query)).scalars().all()] 


def rrf_fuse(rankings: list[list[float]] , weights : int | None = None , k = 60):
    weights = weights or [1.0]*len(rankings)
    scores : dict[str , float] = {}
    for ranking , w in zip(rankings , weights):
        for rank , chunk_id in enumerate(ranking , start=1):
            scores[chunk_id] = scores.get(chunk_id ,0.0) + w /(k+rank)
    return scores         
    

async def retrieve_hybrid(db : AsyncSession , query : str , dense_weight : float = 1.0 , keyword_weight: float = 1.0 , top_k : int = 5 , candidate_k : int = 20 ):

    dense_ranking = await dense_search(db , query , k = candidate_k )
    keyword_ranking = await keyword_search(db , query , k = candidate_k)
    
    fused = rrf_fuse([dense_ranking , keyword_ranking] , weights=[dense_weight , keyword_weight])
    top_res = sorted(fused , key=fused.get , reverse=True)[:top_k]
    if not top_res:
        return []
    
    rows = (await db.execute(select(Knowledge_base).where(Knowledge_base.id.in_(top_res)))).scalars().all()
    by_id = {str(r.id) : r for r in rows}
    dense_posi = {chunk_id : i for i , chunk_id in enumerate(dense_ranking , start = 1)}
    keyword_posi = {chunk_id : i for i , chunk_id in enumerate(keyword_ranking , start = 1)}

    return [Hybrid_chunks(
        id=chunk_id,
        role=by_id[chunk_id].role,
        source=by_id[chunk_id].source,
        chunk_index=by_id[chunk_id].chunk_index,
        chunk_text=by_id[chunk_id].chunk,
        score=fused[chunk_id],
        dense_rank=dense_posi.get(chunk_id),
        keyword_rank=keyword_posi.get(chunk_id)
    ) for chunk_id in top_res]

