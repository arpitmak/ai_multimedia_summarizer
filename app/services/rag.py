# app/services/rag.py

from app.services.retriever import retrieve_chunks
from app.services.llm.openai_llm import llm_complete


def rag_answer(query: str) -> dict:
    chunks = retrieve_chunks(query)

    if not chunks:
        return {"answer": "No relevant context found."}

    context = "\n\n".join(
        f"- {c['text']}" for c in chunks
    )

    prompt = f"""
You are an expert assistant.
Answer the question ONLY using the context below.
If the answer is not in the context, say so clearly.

Context:
{context}

Question:
{query}

Answer:
"""

    answer = llm_complete(prompt)

    return {
        "answer": answer,
        "sources": [
            {
                "chunk_id": c["metadata"]["chunk_id"],
                "source": c["metadata"]["source"],
            }
            for c in chunks
        ],
    }


