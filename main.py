from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routes import transaction, category
from app.scheduler import scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.start()
    yield
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)

app.include_router(transaction.router)
app.include_router(category.router)
