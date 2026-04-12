import logging
from datetime import date
from apscheduler.schedulers.asyncio import AsyncIOScheduler # type: ignore[imoport-untyped]
from app.db.database import SessionLocal
from app.services.report_service import generate_monthly_report

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler(timezone="America/Sao_Paulo")


@scheduler.scheduled_job("cron", day=1, hour=6, minute=0) # type: ignore[misc]
async def monthly_report_job():
    """Roda todo dia 1 às 06:00 e gera o relatório do mês anterior."""
    today = date.today()
    # Calcula o mês anterior corretamente (janeiro → dezembro do ano anterior)
    if today.month == 1:
        year, month = today.year - 1, 12
    else:
        year, month = today.year, today.month - 1

    logger.info(f"[Scheduler] Gerando relatório de {year}-{month:02d}...")
    db = SessionLocal()
    try:
        generate_monthly_report(db, year, month)
    except Exception as e:
        logger.error(f"[Scheduler] Erro ao gerar relatório: {e}")
    finally:
        db.close()