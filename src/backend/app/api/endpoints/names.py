from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.backend.app.api.utils.storage import get_db
from src.backend.app.db.crud.name import (
    create_name,
    delete_name,
    get_name,
    get_names,
    update_name,
)
from src.backend.app.db.database import init_db
from src.backend.app.models.name import NameCreate, NameUpdate, ReadName

router = APIRouter()

init_db()

# not sure if the response model should be read name or name base but ok for now


@router.post("/names/", response_model=ReadName)
async def create_your_name(name_in: NameCreate, db: Session = Depends(get_db)):
    return create_name(db, name_in)


@router.post("/names/", response_model=list[ReadName])
async def read_your_names(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return get_names(db, skip=skip, limit=limit)


@router.post("/names/{name_id}", response_model=ReadName)
async def read_your_name(name_id: int, db: Session = Depends(get_db)):
    name = get_name(db, name_id)
    if not name:
        raise HTTPException(status_code=404, detail="Name not found")
    return name


@router.put("/names/{name_id}", response_model=ReadName)
async def update_your_name(
    name_id: int, name_in: NameUpdate, db: Session = Depends(get_db)
):
    name = get_name(db, name_id)
    if not name:
        raise HTTPException(status_code=404, detail="Name not found")
    updated_name = update_name(db, name, name_in)
    return updated_name


@router.delete("/names/{name_id}", response_model=ReadName)
async def delete_your_name(name_id: int, db: Session = Depends(get_db)):
    name = get_name(db, name_id)
    if not name:
        raise HTTPException(status_code=404, detail="Name not found")
    deleted_name = delete_name(db, name)
    return deleted_name
