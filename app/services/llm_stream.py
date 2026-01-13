# app/services/llm_stream.py
import ollama
from typing import Generator


def stream_llm(prompt: str) -> Generator[str, None, None]:
    """
    Streams tokens from the LLM.
    """
    stream = ollama.chat(
        model="llama3",
        messages=[
            {
                "role": "system",
                "content": "You answer clearly and concisely."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        stream=True
    )

    for chunk in stream:
        yield chunk["message"]["content"]
