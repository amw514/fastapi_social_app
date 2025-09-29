"""add content column to posts table

Revision ID: 432a7f3cffea
Revises: 5c2b7623affe
Create Date: 2025-09-17 16:45:45.352980

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '432a7f3cffea'
down_revision: Union[str, Sequence[str], None] = '5c2b7623affe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts", sa.Column("content",sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts","content")
    pass
