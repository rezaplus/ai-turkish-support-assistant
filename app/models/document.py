from datetime import date

from sqlalchemy import Date, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key=True)
    filename: Mapped[str] = mapped_column(String(255), unique=True)
    title: Mapped[str] = mapped_column(String(255))
    version: Mapped[int] = mapped_column(default=1)
    effective_date: Mapped[date] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String(50), default="active")

    checksum: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True,
    )

    chunks: Mapped[list["DocumentChunk"]] = relationship(
        back_populates="document",
        cascade="all, delete-orphan",
    )