import asyncio
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession
from db.models import Knowledge_base

from sentence_transformers import SentenceTransformer
from sqlalchemy import select

_embedding_model : SentenceTransformer | None = None

def get_embedding_model():
    global _embedding_model
    if not _embedding_model:
        _embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    return _embedding_model    

async def embedd_query(query: str) -> list[float]:
    model = get_embedding_model()
    vect =await asyncio.to_thread(model.encode , query , normalize_embeddings= True)
    return vect.tolist()

@dataclass
class Retrieved_chunks:
    id: str
    role: str
    source: str
    chunk_index: int
    chunk_text : str
    score : float


async def retrieve_chunks(db: AsyncSession , query , top_k = 5 , min_score = None):
    qry_embeddings = await embedd_query(query)
    distance = Knowledge_base.embedding.cosine_distance(qry_embeddings)
    sqlquery = (
        select (Knowledge_base , distance.label("distance")).order_by(distance).limit(top_k)
    )

    rows = (await db.execute(sqlquery)).all()
    results = [
        Retrieved_chunks(
            id=str(row.Knowledge_base.id),
            role=row.Knowledge_base.role,
            source=row.Knowledge_base.source,
            chunk_index=row.Knowledge_base.chunk_index,
            chunk_text=row.Knowledge_base.chunk,
            score=1 - row.distance
        )
        for row in rows
    ]

    if min_score:
        results = [r for r in results if r.score >= min_score]
    return results    

if __name__ == "__main__":
    asyncio.run(retrieve_chunks())
