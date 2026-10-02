from pathlib import Path

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db_session
from app.services.ingestion_service import IngestionService


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.post("/ingest")
async def ingest_documents(
    db: AsyncSession = Depends(get_db_session),
):
    service = IngestionService(db)

    return await service.ingest_all(
        Path("documents")
    )