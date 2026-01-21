from fastapi import APIRouter
from pydantic import BaseModel
from app.services.rag import rag_answer

router = APIRouter()

class QuestionRequest(BaseModel):
    question: str

@router.post("/")
def ask_question(req: QuestionRequest):
    answer = rag_answer(req.question)
    return {"answer": answer}
