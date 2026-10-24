"""add chunks_tsv

Revision ID: 8c9d66d37ac2
Revises: b83b56bda086
Create Date: 2026-10-20 15:43:42.756395

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8c9d66d37ac2'
down_revision: Union[str, Sequence[str], None] = 'b83b56bda086'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        "ALTER TABLE knowledge_chunks ADD COLUMN chunks_tsv tsvector GENERATED ALWAYS AS (to_tsvector('english', chunk)) STORED"
    )
    op.execute(
        "CREATE INDEX ix_knowledge_chunks_tsv ON knowledge_chunks USING gin (chunks_tsv)"
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP INDEX IF EXISTS ix_knowledge_chunks_tsv")
    op.execute("ALTER TABLE knowledge_chunks DROP COLUMN IF EXISTS chunks_tsv")
