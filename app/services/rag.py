from app.services.retriever import retrieve_chunks
import ollama


def build_rag_prompt(context: str, query: str) -> str:
    return f"""
You are a knowledgeable assistant answering questions using ONLY the provided context.

Rules:
- Use only the information in the context below
- If the answer is not in the context, say: "The information is not available in the provided content."
- Do not make up facts
- Be concise and clear

Context:
----------------
{context}
----------------

Question:
{query}

Answer:
"""


def rag_answer(query: str) -> str:
    chunks = retrieve_chunks(query, top_k=4)

    context = "\n\n".join(
        f"[Chunk {i+1}] {c['text']}"
        for i, c in enumerate(chunks)
    )

    prompt = build_rag_prompt(context, query)

    response = ollama.chat(
        model="llama3",
        messages=[
            {"role": "system", "content": "You answer questions from provided lecture notes."},
            {"role": "user", "content": prompt}
        ]
    )

    return response["message"]["content"]
