from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.backend.app.db import base

engine = create_engine(
    "sqlite:///./wedding.db", connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    base.metadata.create_all(bind=engine)
