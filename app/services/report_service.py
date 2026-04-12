import logging
from datetime import datetime, date
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.transaction import Transaction
from app.models.monthly_report import MonthlyReport
from app.enums import TransactionType

logger = logging.getLogger(__name__)


def generate_monthly_report(db: Session, year: int, month: int) -> MonthlyReport | None:
    """
    Agrega as transações de um dado mês e salva o relatório.
    Retorna None se já existir um relatório para esse mês.
    """
    existing = (
        db.query(MonthlyReport)
        .filter(MonthlyReport.year == year, MonthlyReport.month == month)
        .first()
    )
    if existing:
        logger.info(f"Relatório {year}-{month:02d} já existe. Pulando.")
        return None

    # Agrega por type dentro do mês solicitado
    results = (
        db.query(Transaction.type, func.sum(Transaction.amount).label("total"))
        .filter(
            func.extract("year", Transaction.created_at) == year,
            func.extract("month", Transaction.created_at) == month,
        )
        .group_by(Transaction.type)
        .all()
    )

    totals = {row.type: row.total for row in results}
    total_income = totals.get(TransactionType.income, 0.0)
    total_expense = totals.get(TransactionType.expense, 0.0)

    report = MonthlyReport(
        year=year,
        month=month,
        total_income=total_income,
        total_expense=total_expense,
        net=total_income - total_expense,
        generated_at=datetime.utcnow(),
    )

    db.add(report)
    db.commit()
    db.refresh(report)

    logger.info(
        f"Relatório {year}-{month:02d} gerado: "
        f"receitas={total_income}, despesas={total_expense}, saldo={report.net}"
    )
    return report