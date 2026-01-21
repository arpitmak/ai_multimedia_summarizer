# app/services/rag_stream.py

from typing import Generator
from app.services.retriever import retrieve_chunks
from app.services.llm.openai_llm import llm_stream


def rag_stream_answer(query: str) -> Generator[str, None, None]:
    chunks = retrieve_chunks(query)

    if not chunks:
        yield "No relevant context found."
        return

    context = "\n\n".join(
        f"- {c['text']}" for c in chunks
    )

    prompt = f"""
You are an expert assistant.
Answer the question ONLY using the context below.

Context:
{context}

Question:
{query}

Answer:
"""

    for token in llm_stream(prompt):
        yield token


