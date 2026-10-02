from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.providers.ollama_embedding import OllamaEmbeddingProvider
from app.core.config import get_settings


@dataclass
class SearchResult:
    content: str
    section: str | None
    filename: str
    title: str
    version: int
    status: str
    distance: float


class RetrievalService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.embedding_provider = OllamaEmbeddingProvider()
        self.settings = get_settings()

    async def search(
        self,
        query: str,
        limit: int = 5,
    ) -> list[SearchResult]:
        query_embedding = await self.embedding_provider.embed(query)

        distance = DocumentChunk.embedding.cosine_distance(
            query_embedding
        )

        statement = (
            select(
                DocumentChunk,
                Document,
                distance.label("distance"),
            )
            .join(
                Document,
                Document.id == DocumentChunk.document_id,
            )
            .where(Document.status == "active")
            .order_by(distance)
            .limit(limit)
        )

        result = await self.db.execute(statement)

        return [
            SearchResult(
                content=chunk.content,
                section=chunk.section,
                filename=document.filename,
                title=document.title,
                version=document.version,
                status=document.status,
                distance=float(distance_value),
            )
            for chunk, document, distance_value in result.all()
        ]
    def is_relevant(self, results: list[SearchResult]) -> bool:
        if not results:
            return False

        best_result = results[0]

        return best_result.distance <= self.settings.retrieval_max_distance