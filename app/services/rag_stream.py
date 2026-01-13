# app/services/rag_stream.py
from typing import Generator
from app.services.retriever import retrieve_chunks
from app.services.llm_stream import stream_llm


def build_streaming_rag_prompt(context: str, query: str) -> str:
    return f"""
You are an assistant answering a question using the provided context.

Rules:
- Answer directly and progressively
- Use short, clear sentences
- Use ONLY the context
- If answer not found, say so clearly

Context:
----------------
{context}
----------------

Question:
{query}

Start answering now:
"""


def rag_stream_answer(query: str) -> Generator[str, None, None]:
    chunks = retrieve_chunks(query, top_k=4)

    if not chunks:
        yield "I could not find relevant information for your question."
        return

    context = "\n\n".join(c["text"] for c in chunks)

    prompt = build_streaming_rag_prompt(context, query)

    yield from stream_llm(prompt)
