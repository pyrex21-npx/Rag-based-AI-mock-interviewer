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

async def keyword_search():
    pass

async def dense_search():
    pass


def rrf_fuse():
    pass

async def retrieve_hybrid():
    pass