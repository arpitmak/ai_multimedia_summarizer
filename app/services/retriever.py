from typing import List, Dict
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

# 🔒 MUST match vector_store.py
CHROMA_DIR = "storage/chroma"
COLLECTION_NAME = "multimedia_chunks"

# Load embedding model once
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def retrieve_chunks(
    query: str,
    top_k: int = 5
) -> List[Dict]:
    """
    Retrieve top-k relevant chunks for a user query.
    """

    # Embed query
    query_embedding = embedding_model.encode(query).tolist()

    # Persistent Chroma client
    client = chromadb.PersistentClient(
        path=CHROMA_DIR,
        settings=Settings(anonymized_telemetry=False)
    )

    collection = client.get_collection(name=COLLECTION_NAME)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    retrieved_chunks = []

    for i in range(len(results["documents"][0])):
        retrieved_chunks.append({
            "text": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i]
        })

    return retrieved_chunks
