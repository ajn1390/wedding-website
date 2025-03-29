from sqlalchemy.orm import Session

from src.backend.app.db.models.name import Name
from src.backend.app.models.name import NameCreate, NameUpdate

# from models.name import NameCreate, NameUpdate


def create_name(db: Session, name_in: NameCreate) -> Name:
    db_name = Name(
        first_name=name_in.first_name,
        last_name=name_in.last_name,
        alternate_first_name=name_in.alternate_first_name,
        alternate_last_name=name_in.alternate_last_name,
    )
    db.add(db_name)
    db.commit()
    db.refresh(db_name)
    return db_name


def get_name(db: Session, name_id: int) -> Name | None:
    return db.query(Name).filter(Name.id == name_id).first()


def get_names(db: Session, skip: int = 0, limit: int = 100) -> list[Name]:
    return db.query(Name).offset(skip).limit(limit).all()


def update_name(db: Session, db_name: Name, name_in: NameUpdate) -> Name:
    if name_in.first_name is not None:
        db_name.first_name = name_in.first_name
    if name_in.last_name is not None:
        db_name.last_name = name_in.last_name
    if name_in.alternate_first_name is not None:
        db_name.alternate_first_name = name_in.alternate_first_name
    if name_in.alternate_last_name is not None:
        db_name.alternate_last_name = name_in.alternate_last_name

    db.commit()
    db.refresh(db_name)
    return db_name


def delete_name(db: Session, db_name: Name) -> Name:
    db.delete(db_name)
    db.commit()
    return db_name
