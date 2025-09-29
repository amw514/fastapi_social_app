"""create posts table

Revision ID: 5c2b7623affe
Revises: 
Create Date: 2025-09-17 16:44:04.188632

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5c2b7623affe'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("posts",
                    sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
                    sa.Column("title", sa.String(), nullable=False),
                    # sa.Column("published", sa.Boolean(), nullable=False, server_default="TRUE"),
                    # sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")),
                    # sa.Column("owner_id", sa.Integer(), nullable=False),
                    # sa.ForeignKeyConstraint(["owner_id"], ["users.id"], ondelete="CASCADE"),
                    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("posts")
    pass
