from fastapi import FastAPI

from src.backend.app.api.endpoints import names
from src.backend.app.db.database import init_db

app = FastAPI(title="Project")

init_db()

app.include_router(names.router, prefix="/names", tags=["Names"])


@app.get("/")
def read_root():
    return {"message": "Hello"}
