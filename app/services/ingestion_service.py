from pathlib import Path
import hashlib
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.providers.ollama_embedding import OllamaEmbeddingProvider
from app.services.document_parser import parse_markdown_document


class IngestionService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.embedding_provider = OllamaEmbeddingProvider()

    async def ingest_all(self, directory: Path) -> dict:
        files = sorted(directory.glob("*.md"))

        created = 0
        updated = 0
        skipped = 0

        for file_path in files:
            result = await self.ingest(file_path)

            if result == "created":
                created += 1
            elif result == "updated":
                updated += 1
            elif result == "skipped":
                skipped += 1

        await self.db.commit()

        return {
            "processed": len(files),
            "created": created,
            "updated": updated,
            "skipped": skipped,
        }

    def _calculate_checksum(self, file_path: Path) -> str:
        content = file_path.read_bytes()

        return hashlib.sha256(content).hexdigest()

    async def ingest(self, file_path: Path) -> str:
        checksum = self._calculate_checksum(file_path)
        parsed = parse_markdown_document(file_path)

        result = await self.db.execute(
            select(Document)
            .options(selectinload(Document.chunks))
            .where(Document.filename == parsed.filename)
        )

        document = result.scalar_one_or_none()

        if document and document.checksum == checksum:
            return "skipped"

        if document:
            document.title = parsed.title
            document.version = parsed.version
            document.status = parsed.status
            document.effective_date = parsed.effective_date
            document.checksum = checksum

            # Remove old chunks before regenerating embeddings.
            for chunk in document.chunks:
                await self.db.delete(chunk)

            await self.db.flush()

            action = "updated"

        else:
            document = Document(
                filename=parsed.filename,
                title=parsed.title,
                version=parsed.version,
                status=parsed.status,
                effective_date=parsed.effective_date,
                checksum=checksum
            )

            self.db.add(document)

            # We need the generated document.id before creating chunks.
            await self.db.flush()

            action = "created"

        for index, section in enumerate(parsed.sections):
            embedding_text = f"""
        Document: {parsed.title}
        Section: {section.title}

        {section.content}
        """.strip()

            embedding = await self.embedding_provider.embed(embedding_text)

            chunk = DocumentChunk(
                document_id=document.id,
                chunk_index=index,
                section=section.title,
                page=None,
                content=section.content,
                embedding=embedding,
            )

            self.db.add(chunk)

        return action