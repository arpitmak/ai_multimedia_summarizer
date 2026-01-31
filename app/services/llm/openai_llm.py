from typing import Generator
from openai import OpenAI
from app.core.config import settings

if not settings.openrouter_api_key:
    raise RuntimeError("OPENROUTER_API_KEY is missing. Check your .env and app startup loading.")

client = OpenAI(
    api_key=settings.openrouter_api_key,
    base_url="https://openrouter.ai/api/v1",
)

MODEL = "arcee-ai/trinity-large-preview:free"

def llm_complete(prompt: str) -> str:
    res = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        extra_headers={
            "HTTP-Referer": settings.openrouter_site_url,
            "X-Title": settings.openrouter_app_name,
        },
    )
    return res.choices[0].message.content or ""

def llm_stream(prompt: str) -> Generator[str, None, None]:
    stream = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        stream=True,
        extra_headers={
            "HTTP-Referer": settings.openrouter_site_url,
            "X-Title": settings.openrouter_app_name,
        },
    )
    for chunk in stream:
        if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content
