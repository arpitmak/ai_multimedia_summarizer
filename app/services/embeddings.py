from sentence_transformers import SentenceTransformer
from typing import List

# Small, fast, free, widely used
MODEL_NAME = "all-MiniLM-L6-v2"

_model = None


def get_embedding_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model


def embed_texts(texts: List[str]) -> List[List[float]]:
    model = get_embedding_model()
    embeddings = model.encode(texts, show_progress_bar=False)
    return embeddings.tolist()
 