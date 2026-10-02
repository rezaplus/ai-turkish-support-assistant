"""add checksum to documents

Revision ID: 28d7addf8750
Revises: 2f988392ee90
Create Date: 2026-10-02
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "28d7addf8750"
down_revision: Union[str, Sequence[str], None] = "2f988392ee90"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add the nullable checksum used to skip unchanged documents."""
    op.add_column(
        "documents",
        sa.Column("checksum", sa.String(length=64), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("documents", "checksum")
