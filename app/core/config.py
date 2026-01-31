# app/core/config.py
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).resolve().parents[2]  # project root (ai_multimedia_summarizer/)
ENV_PATH = ROOT_DIR / ".env"

class Settings(BaseSettings):
    app_name: str = "AI Multimedia Note Summarizer"
    app_env: str = "development"
    log_level: str = "INFO"

    openrouter_api_key: str | None = None
    openrouter_site_url: str = "http://localhost"
    openrouter_app_name: str = "ai-multimedia-summarizer"

    model_config = SettingsConfigDict(env_file=str(ENV_PATH), extra="ignore")

settings = Settings()
