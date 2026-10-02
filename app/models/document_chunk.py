from pgvector.sqlalchemy import Vector
from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id: Mapped[int] = mapped_column(primary_key=True)

    document_id: Mapped[int] = mapped_column(
        ForeignKey("documents.id", ondelete="CASCADE")
    )

    chunk_index: Mapped[int] = mapped_column(Integer)
    page: Mapped[int | None] = mapped_column(Integer, nullable=True)
    section: Mapped[str | None] = mapped_column(Text, nullable=True)

    content: Mapped[str] = mapped_column(Text)

    embedding: Mapped[list[float]] = mapped_column(
        Vector(1024)
    )

    document: Mapped["Document"] = relationship(
        back_populates="chunks"
    )