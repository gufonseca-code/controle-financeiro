from pydantic import BaseModel
from app.enums import TransactionType

class CategoryCreate(BaseModel):
    name: str
    type: TransactionType

class CategoryResponse(CategoryCreate):
    id: int

    class Config:
        from_attributes = True