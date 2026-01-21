from fastapi import FastAPI
from app.core.config import settings
from app.core.logger import logger
from app.api.routes.health import router as health_router
from app.api.routes.ingest import router as ingest_router
from app.api.routes.query import router as query_router
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import summary
from app.api.routes import qa
app = FastAPI(
    title=settings.app_name,
    description="Backend API for RAG-based multimedia summarization",
    version="0.1.0"
)





app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/api/v1")
app.include_router(ingest_router, prefix="/api/v1/ingest")
app.include_router(
    query_router,
    prefix="/api/v1",
    tags=["Query"]
)
app.include_router(summary.router, prefix="/api/v1",tags=["summary"])
app.include_router(qa.router,prefix="/qa", tags=["QnA"])


@app.on_event("startup")
def startup_event():
    logger.info("Application starting...")
