from fastapi import FastAPI
from app.core.config import settings
from app.core.logger import logger
from app.api.routes.health import router as health_router
from app.api.routes.ingest import router as ingest_router

app = FastAPI(
    title=settings.app_name,
    description="Backend API for RAG-based multimedia summarization",
    version="0.1.0"
)

app.include_router(health_router, prefix="/api/v1")
app.include_router(ingest_router, prefix="/api/v1/ingest")


@app.on_event("startup")
def startup_event():
    logger.info("Application starting...")
