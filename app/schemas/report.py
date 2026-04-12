from pydantic import BaseModel
from datetime import datetime


class MonthlyReportResponse(BaseModel):
    id: int
    year: int
    month: int
    total_income: float
    total_expense: float
    net: float
    generated_at: datetime

    class Config:
        from_attributes = True