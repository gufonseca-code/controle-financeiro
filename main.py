from fastapi import FastAPI

from app.db.database import Base, engine
from app.routes import transaction, category

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(transaction.router)
app.include_router(category.router)
