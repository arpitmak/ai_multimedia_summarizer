from app.schemas.query import QueryRequest, QueryResponse
from fastapi.responses import StreamingResponse
from app.services.rag_stream import rag_stream_answer
from app.services.rag import rag_answer
from fastapi import APIRouter
router = APIRouter()

@router.post("/query", response_model=QueryResponse)
def query_rag(data: QueryRequest):
    answer = rag_answer(data.query)
    return {"answer": answer}

@router.post("/query/stream")
def query_stream(payload: QueryRequest):
    return StreamingResponse(
        rag_stream_answer(payload.query),
        media_type="text/plain"
    )
