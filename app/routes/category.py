from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryResponse
from app.enums import TransactionType

router = APIRouter(prefix="/categories", tags=["Categories"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=CategoryResponse)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    db_category = Category(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@router.get("/", response_model=list[CategoryResponse])
def get_categories(type: TransactionType | None = None, db: Session = Depends(get_db)):
    query = db.query(Category)
    if type:
        query = query.filter(Category.type == type)
    return query.all()

@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(category)
    db.commit()
    return {"message": "Deleted successfully"}