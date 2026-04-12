"""add created_at to transactions

Revision ID: d9b2e1034c67
Revises: c3a1f0712b45
Create Date: 2026-04-11 10:30:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "d9b2e1034c67"
down_revision: Union[str, None] = "c3a1f0712b45"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "transactions",
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )


def downgrade() -> None:
    op.drop_column("transactions", "created_at")