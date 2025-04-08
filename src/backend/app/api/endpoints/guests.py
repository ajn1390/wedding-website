from fastapi import APIRouter

from src.backend.app.db.database import init_db

router = APIRouter()

init_db()
