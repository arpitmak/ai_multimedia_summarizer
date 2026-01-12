from sentence_transformers import SentenceTransformer
from typing import List, Dict

# Free, fast, CPU-friendly
MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


def embed_chunks(chunks: List[Dict]) -> List[List[float]]:
    """
    Generate embeddings for chunk texts.
    """
    texts = [chunk["text"] for chunk in chunks]
    embeddings = model.encode(texts, show_progress_bar=True)
    return embeddings.tolist()
