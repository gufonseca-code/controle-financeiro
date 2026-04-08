from pydantic import BaseModel, field_validator
from app.enums import TransactionType
from app.schemas.category import CategoryResponse

class TransactionCreate(BaseModel):
    title: str
    amount: float
    type: TransactionType
    category_id: int | None = None

    @field_validator("amount")
    @classmethod
    def amount_must_be_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("amount must be greater than zero")
        return v

class TransactionResponse(BaseModel):
    id: int
    title: str
    amount: float
    type: TransactionType
    category: CategoryResponse | None = None

    class Config:
        from_attributes = True