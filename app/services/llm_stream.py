# app/services/llm_stream.py

from typing import Generator
from app.services.llm.openai_llm import llm_stream


def stream_llm(prompt: str) -> Generator[str, None, None]:
    return llm_stream(prompt)

