import chromadb
from pathlib import Path
from typing import List, Dict

CHROMA_DIR = "storage/vectors"
COLLECTION_NAME = "multimedia_chunks"


def get_collection():
    Path(CHROMA_DIR).mkdir(parents=True, exist_ok=True)

    client = chromadb.PersistentClient(path=CHROMA_DIR)

    return client.get_or_create_collection(
        name=COLLECTION_NAME
    )


def store_chunks(chunks: List[Dict], embeddings: List[List[float]]):
    collection = get_collection()

    collection.add(
        ids=[f"chunk_{c['chunk_id']}" for c in chunks],
        documents=[c["text"] for c in chunks],
        metadatas=[
            {
                "source": c["source"],
                "start_time": c["start_time"],
                "end_time": c["end_time"],
            }
            for c in chunks
        ],
        embeddings=embeddings,
    )
