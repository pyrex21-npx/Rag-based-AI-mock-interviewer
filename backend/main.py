from fastapi import FastAPI , HTTPException , UploadFile 
from fastapi.middleware.cors import CORSMiddleware
from pypdf import PdfReader
from io import BytesIO
from sentence_transformers import SentenceTransformer

app = FastAPI()
model = SentenceTransformer("all-MiniLM-L6-v2")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status" : "ok"} 

@app.post("/api/upload")
async def upload_pdf(file : UploadFile):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400 , detail="The document tyoe is invalid")
    
    content = await file.read()

    try:
        reader = PdfReader(BytesIO(content))
        text = "\n".join(page.extract_text() for page in reader.pages)
    except Exception as e:
        raise HTTPException(status_code=422 , detail="Could not parse pdf: {e}")
    if not text.strip():
        raise HTTPException(status_code=422 , detail="No text could be extracted")  
    print(text)  
    return {
        "filename" : file.filename , 
        "num_of_page" : len(reader.pages),
        "extracted_data" : text 
    }




