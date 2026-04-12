from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.monthly_report import MonthlyReport
from app.schemas.report import MonthlyReportResponse
from app.services.report_service import generate_monthly_report

router = APIRouter(prefix="/reports", tags=["Reports"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/monthly", response_model=list[MonthlyReportResponse])
def list_reports(db: Session = Depends(get_db)):
    return db.query(MonthlyReport).order_by(MonthlyReport.year.desc(), MonthlyReport.month.desc()).all()


@router.post("/monthly/generate", response_model=MonthlyReportResponse)
def trigger_report(year: int, month: int, db: Session = Depends(get_db)):
    """Endpoint manual para gerar um relatório de qualquer mês. Útil para testes."""
    if not (1 <= month <= 12):
        raise HTTPException(status_code=422, detail="Mês deve ser entre 1 e 12")

    report = generate_monthly_report(db, year, month)
    if report is None:
        raise HTTPException(status_code=409, detail="Relatório para esse mês já existe")
    return report