# app/services/vector_store.py

from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions

BASE_DIR = Path(__file__).resolve().parents[2]
CHROMA_DIR = BASE_DIR / "storage" / "chroma"

# SentenceTransformer embedding (free, local)
embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# Persistent Chroma client
client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)

collection = client.get_or_create_collection(
    name="multimedia_chunks",
    embedding_function=embedding_fn
)

def store_chunks(chunks):
    print(f"Adding vectors: {len(chunks)}")

    ids = [
        f"{c['source']}_{c['chunk_id']}"
        for c in chunks
    ]

    documents = [c["text"] for c in chunks]

    metadatas = [
        {
            "chunk_id": c["chunk_id"],
            "source": c["source"],
            "start_time": c["start_time"],
            "end_time": c["end_time"],
        }
        for c in chunks
    ]

    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )

    print("Stored successfully")
