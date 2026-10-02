from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db_session
from app.services.rag_service import RAGService


router = APIRouter(prefix="/ask", tags=["Assistant"])


class AskRequest(BaseModel):
    question: str = Field(min_length=2)


@router.post("")
async def ask(
    request: AskRequest,
    db: AsyncSession = Depends(get_db_session),
):
    rag = RAGService(db)

    result = await rag.answer(request.question)

    return {
        "question": request.question,
        **result,
    }