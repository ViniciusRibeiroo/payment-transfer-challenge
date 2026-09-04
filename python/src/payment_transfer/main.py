from fastapi import FastAPI
from payment_transfer.infrastructure.database import initialize_database

app = FastAPI(
    title="Payment Transfer Challenge",
    version="0.1.0",
)


@app.on_event("startup")
def startup() -> None:
    initialize_database()


@app.get("/health")
def health_check():
    return {"status": "ok"}
