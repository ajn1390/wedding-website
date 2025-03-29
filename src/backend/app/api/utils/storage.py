"""
Database-related utilities for the API.
"""

from src.backend.app.db.database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
