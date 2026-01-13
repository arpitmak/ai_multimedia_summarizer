import json
from pathlib import Path
from sentence_transformers import SentenceTransformer
import chromadb

# paths
BASE_DIR = Path(__file__).resolve().parent
CHUNKS_DIR = BASE_DIR / "storage" / "chunks"
CHROMA_DIR = BASE_DIR / "storage" / "chroma"

# load chunks file
chunk_file = list(CHUNKS_DIR.glob("*.json"))[0]
transcript_name = chunk_file.stem.replace("_chunks", "")

with open(chunk_file, "r", encoding="utf-8") as f:
    chunks = json.load(f)

print(f"Loaded chunks: {len(chunks)}")

# embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")
texts = [c["text"] for c in chunks]

embeddings = model.encode(texts, show_progress_bar=True).tolist()
print("Embeddings generated")

# prepare metadata (IMPORTANT)
metadatas = [
    {
        "chunk_id": c["chunk_id"],
        "start_time": c["start_time"],
        "end_time": c["end_time"],
        "source": c.get("source", "unknown"),
        "transcript": transcript_name,
    }
    for c in chunks
]

# chroma (NEW API)
client = chromadb.PersistentClient(path=str(CHROMA_DIR))

collection = client.get_or_create_collection(
    name="multimedia_chunks"
)

collection.add(
    ids=[f"{transcript_name}_{c['chunk_id']}" for c in chunks],
    documents=texts,
    embeddings=embeddings,
    metadatas=metadatas,  # ✅ THIS IS THE FIX
)

print("Stored in Chroma")

# sanity check
print("Chroma count:", collection.count())
