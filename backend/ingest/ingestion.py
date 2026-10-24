import asyncio
import numpy
from pathlib import Path
from ingest.text_extraction import extract_text_from_file
from ingest.Chunker import semantic_chunking
from sentence_transformers import SentenceTransformer
from db.base import asyncsession
from db.models import Knowledge_base
import uuid


BOOK_DIR = Path(__file__).parent.parent / "books"

print(BOOK_DIR , BOOK_DIR.exists() , list(BOOK_DIR.glob("*.pdf"))) 

role_to_books = {
    "ai_ml" : ["2019Burkovaiml.pdf"],
    # "backend" : "" ,
    # "frontend" : "",
    # "testing" : "",
    # "security" : "",
    # "devops" : "",
    # "cloud_&_infrastructure" : "" ,
    # "data_engineer" : "",
    # "database" : "" , 
    # "site_reliability" : "",
    # "mobile" : "" ,
    # "data_science" : ""
}

async def ingest_doc():
    embedding_model=SentenceTransformer("all-MiniLM-L6-v2")

    async with asyncsession() as session:
        for role , books in role_to_books.items():
            if not books:
                print("No books configured for this role")
                continue
            for book in books:
                book_path = BOOK_DIR / book
                if not book_path.exists():
                    print(f"The {book} is not available")
                    continue
            
                extracted_book = extract_text_from_file(str(book_path))
                chunks = semantic_chunking(extracted_book , embedding_model=embedding_model , base_metadata={"role" : role , "source" : book})
                text = [c.text for c in chunks]
                embeddings = embedding_model.encode(
                    text,
                    normalize_embeddings=True,
                    show_progress_bar=True,
                    batch_size=32 
                ) 
                

                for chunk , embedding in zip(chunks , embeddings):
                    db_row = Knowledge_base(
                        id = uuid.uuid4(),
                        role= chunk.metadata["role"],
                        source= chunk.metadata["source"],
                        chunk= chunk.text,
                        chunk_index= chunk.metadata["chunk_index"],
                        embedding= embedding.tolist(),

                    )
                    session.add(db_row)

                await session.commit()


if __name__ == "__main__":
    asyncio.run(ingest_doc())