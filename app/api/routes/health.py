from fastapi import APIRouter
from app.core.logger import logger

router = APIRouter()


@router.get("/health")
def health_check():
    logger.info("Health check called")
    return {"status": "ok"}
