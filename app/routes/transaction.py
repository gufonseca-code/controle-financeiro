from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.category import Category
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionResponse

router = APIRouter(prefix="/transactions", tags=["Transactions"])

# Dependency para abrir/fechar sessão
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def validate_category(
    category_id: int | None, transaction_type: str, db: Session
) -> Category | None:
    if category_id is None:
        return None

    category = db.query(Category).filter(Category.id == category_id).first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    if category.type != transaction_type:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Category '{category.name}' belongs to '{category.type}', "
                f"not '{transaction_type}'"
            ),
        )

    return category

# CREATE
@router.post("/", response_model=TransactionResponse)
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    validate_category(transaction.category_id, transaction.type, db)

    db_transaction = Transaction(**transaction.model_dump())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

# READ ALL
@router.get("/", response_model=list[TransactionResponse])
def get_transactions(db: Session = Depends(get_db)):
    return db.query(Transaction).all()

# READ BY ID
@router.get("/{transaction_id}", response_model=TransactionResponse)
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

# UPDATE
@router.put("/{transaction_id}", response_model=TransactionResponse)
def update_transaction(transaction_id: int, data: TransactionCreate, db: Session = Depends(get_db)):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()

    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    validate_category(data.category_id, data.type, db)

    transaction.title = data.title
    transaction.amount = data.amount
    transaction.type = data.type
    transaction.category_id = data.category_id

    db.commit()
    db.refresh(transaction)
    return transaction

# DELETE
@router.delete("/{transaction_id}")
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()

    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    db.delete(transaction)
    db.commit()

    return {"message": "Deleted successfully"}
