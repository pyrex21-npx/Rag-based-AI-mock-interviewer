from dataclasses import dataclass , field
import re
from sentence_transformers import SentenceTransformer
import numpy as np
import uuid

#Fixed size chunking

@dataclass
class Chunk:
    text: str
    metadata : dict = field(default_factory=dict)


def fixed_size(extracted_text : str , chunk_size : int = 500 , chunk_overlap : int = 50 , base_metadata : dict | None = None):
    base_metadata = base_metadata or {}
    words = extracted_text.split()
    chunks = []
    diff = chunk_size - chunk_overlap
    chunk_index = 0

    if diff <=0 :
        raise ValueError("The overlap must be smaller than chunk size")

    for st in range(0 , len(words) , diff):
        chunk_words = words[st:min(st + chunk_size , len(words))]
        if not chunk_words:
            break
        chunk_text = " ".join(chunk_words)
        chunks.append(Chunk(text=chunk_text , metadata={**base_metadata , "chunk_index" : chunk_index ,"id" : str(uuid.uuid4()) }))
        chunk_index += 1
        if st + chunk_size >= len(extracted_text):
            break
        # chunks.append(Chunk(text = " ".join(words[st:])))
    return chunks


#Semantic Chunking


def split_into_sentences(extracted_text : str):

    sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z])', extracted_text.strip())
    return [s.strip() for s in sentences if s.strip()]

def semantic_chunking(
        text : str ,
        embedding_model : SentenceTransformer ,
        sim_threshold : float = 0.5 , 
        max_chunk_size : int = 2000 ,
        min_chunk_size : int = 200 , 
        base_metadata : dict | None = None
):
    base_metadata = base_metadata or {}
    sentences = split_into_sentences(text)
    if len(sentences) <= 1:
        return [Chunk(text=text)]

    embeddings = embedding_model.encode(sentences , convert_to_numpy=True , normalize_embeddings=True)

    chunks = []
    curr_sentence = [sentences[0]]
    for i in range(1 , len(sentences)):
        sim = np.dot(embeddings[i] , embeddings[i-1])

        curr_text = " ".join(curr_sentence)
        ifmaxlen = (len(curr_text) + len(sentences[i]) )  > max_chunk_size

        if (sim < sim_threshold or ifmaxlen) and len(curr_text) >= min_chunk_size:
            chunks.append(Chunk(text = curr_text , metadata={**base_metadata , "chunk_index" : len(chunks) , "id" : uuid.uuid4()}))
            curr_sentence = [sentences[i]]
        else:
            curr_sentence.append(sentences[i])
    if curr_sentence:
        chunks.append(Chunk(text= " ".join(curr_sentence) , metadata={**base_metadata , "chunk_index" : len(chunks) , "id" : uuid.uuid4()}))

    return chunks    




