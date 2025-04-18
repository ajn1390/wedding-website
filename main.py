from fastapi import FastAPI

from src.backend.app.api.endpoints import endpoints
from src.backend.app.db.database import init_db

app = FastAPI(title="Project")

init_db()

app.include_router(endpoints.router, prefix="/endpoints", tags=["Endpoints"])


@app.get("/")
def read_root():
    return {"message": "Hello"}
