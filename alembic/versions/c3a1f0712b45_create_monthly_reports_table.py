"""create monthly reports table

Revision ID: c3a1f0712b45
Revises: a4d2e0890be8
Create Date: 2026-04-11 10:00:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "c3a1f0712b45"
down_revision: Union[str, None] = "a4d2e0890be8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "monthly_reports",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("month", sa.Integer(), nullable=False),
        sa.Column("total_income", sa.Float(), nullable=False),
        sa.Column("total_expense", sa.Float(), nullable=False),
        sa.Column("net", sa.Float(), nullable=False),
        sa.Column("generated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("year", "month", name="uq_monthly_reports_year_month"),
    )
    op.create_index(op.f("ix_monthly_reports_id"), "monthly_reports", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_monthly_reports_id"), table_name="monthly_reports")
    op.drop_table("monthly_reports")