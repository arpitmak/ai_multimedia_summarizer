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
You must answer using ONLY the provided context.
If the answer is not present in the context, say:
"Not found in the ingested content."
Do not use outside knowledge.

Context:
{context}

Question:
{query}

Answer:
"""

    for token in llm_stream(prompt):
        yield token


