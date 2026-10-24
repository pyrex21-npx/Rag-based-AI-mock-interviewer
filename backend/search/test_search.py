import asyncio
from db.base import asyncsession
from search.dense_search import retrieve_chunks

TEST_QUERIES = [
    "What is overfitting and how do you prevent it?",
    "Explain the difference between supervised and unsupervised learning",
    "How does gradient descent work?",
    "What is regularization?",
    "How do you evaluate a classification model?",
]


async def main():
    async with asyncsession() as db:
        for q in TEST_QUERIES:
            print(f"\n=== {q}")
            for r in await retrieve_chunks(db, q, top_k=3):
                preview = r.chunk_text[:200].replace("\n", " ")
                print(f"[{r.score:.3f}] {r.source}#{r.chunk_index}: {preview}...")



if __name__ == "__main__":
    asyncio.run(main())