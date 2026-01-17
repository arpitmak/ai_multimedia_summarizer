# app/services/summarizer.py

from typing import Generator, List, Dict
from app.services.llm_stream import stream_llm


def stream_summary(
    chunks: List[Dict]
) -> Generator[str, None, None]:
    """
    Stream summary from already-prepared chunks.
    """

    if not chunks:
        yield "No content to summarize."
        return

    yield "### Summary\n\n"

    for chunk in chunks:
        prompt = f"""
SYSTEM INSTRUCTIONS (DO NOT SUMMARIZE THIS):
You are a professional technical summarizer.Avoid repetition across chunks.Be concise and accurate

{chunk['text']}

Summary:
"""

        for token in stream_llm(prompt):
            yield token

        yield "\n\n"

