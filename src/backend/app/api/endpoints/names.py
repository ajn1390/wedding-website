import typing as tp

from fastapi import FastAPI, Depends

from src.backend.app.models.name import NameCreate
from src.backend.app.db.models import Name, NameCreate
from src.backend.app.api.utils.storage import get_db
from sqlalchemy.orm import Session

app = FastAPI()

@app.post("/names/", response_model=NameCreate)
async def create_name(name: NameCreate, db: Session = Depends(get_db)):
    db_name = Name(**name.dict())
    # db.add(db_name)
    # db.commit()
    # db.refresh(db_name)
    # return db_name