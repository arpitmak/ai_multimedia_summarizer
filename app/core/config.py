from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "AI Multimedia Note Summarizer"
    app_env: str = "development"
    log_level: str = "INFO"

    class Config:
        env_file = ".env"


settings = Settings()
