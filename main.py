from fastapi import FastAPI

from app.routes import transaction, category

app = FastAPI()

app.include_router(transaction.router)
app.include_router(category.router)
