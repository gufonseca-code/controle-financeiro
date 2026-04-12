from datetime import datetime
from sqlalchemy import Integer, Float, DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base


class MonthlyReport(Base):
    __tablename__ = "monthly_reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    month: Mapped[int] = mapped_column(Integer, nullable=False)
    total_income: Mapped[float] = mapped_column(Float, nullable=False)
    total_expense: Mapped[float] = mapped_column(Float, nullable=False)
    net: Mapped[float] = mapped_column(Float, nullable=False)
    generated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    __table_args__ = (
        UniqueConstraint("year", "month", name="uq_monthly_reports_year_month"),
    )