from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .config import STATIC_PATH
from .database import initialize_database
from .routers.expenses import router as expenses_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    yield


app = FastAPI(title="MyExpense", description="Personal expense management", lifespan=lifespan)
app.mount("/static", StaticFiles(directory=STATIC_PATH), name="static")
app.include_router(expenses_router)
