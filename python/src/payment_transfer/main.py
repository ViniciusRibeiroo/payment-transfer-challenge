from contextlib import asynccontextmanager

from fastapi import FastAPI

from payment_transfer.api.transfers import router as transfers_router
from payment_transfer.infrastructure.database import initialize_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    yield


app = FastAPI(
    title="Payment Transfer Challenge",
    version="0.1.0",
    lifespan=lifespan,
)


app.include_router(transfers_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
