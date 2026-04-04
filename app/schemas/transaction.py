from pydantic import BaseModel

class TransactionCreate(BaseModel):
    title: str
    amount: float
    type: str

class TransactionResponse(TransactionCreate):
    id: int

    class Config:
        from_attributes = True