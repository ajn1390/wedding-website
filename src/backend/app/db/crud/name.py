from typing import Optional

from fastapi import HTTPException
from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.backend.app.db.models.name import Name
from src.backend.app.models.name import NameAdmin, NameCreate, NameUpdate

# from models.name import NameCreate, NameUpdate


def admin_create_name(db: Session, name_in: NameAdmin) -> Name:
    # db_name = Name(
    #     first_name=name_in.first_name,
    #     last_name=name_in.last_name,
    #     alternate_first_name=name_in.alternate_first_name,
    #     alternate_last_name=name_in.alternate_last_name,
    # )
    matches = (
        db.query(Name)
        .filter(
            and_(
                Name.first_name.ilike(name_in.first_name),
                Name.last_name.ilike(name_in.last_name),
            )
        )
        .all()
    )

    if matches and not name_in.dup_record_answer:
        raise HTTPException(
            status_code=400, detail="Duplicate name found. Provide an answer"
        )
        # if not name_in.dup_record_answer:
        #     q = "What is the full name of your city of residence?"
        #     raise HTTPException(status_code=400, detail=f" Name Found. {q}")
        # name_in_data["dup_record_question"] = q

    db_name = Name(
        first_name=name_in.first_name,
        last_name=name_in.last_name,
        alternate_first_name=",".join(name_in.alternate_first_name)
        if name_in.alternate_first_name
        else None,
        alternate_last_name=",".join(name_in.alternate_last_name)
        if name_in.alternate_last_name
        else None,
        dup_record_question="Full name of their resident city" if matches else None,
        dup_record_answer=name_in.dup_record_answer if matches else None,
    )

    db.add(db_name)
    db.commit()
    db.refresh(db_name)
    return db_name


def create_name(db: Session, name_in: NameCreate) -> Name:
    matches = (
        db.query(Name)
        .filter(
            and_(
                Name.first_name.ilike(name_in.first_name),
                Name.last_name.ilike(name_in.last_name),
            )
        )
        .all()
    )

    name_in_data = name_in.model_dump()

    if matches:
        if not name_in.dup_record_answer:
            q = "What is the full name of your city of residence?"
            raise HTTPException(status_code=400, detail=f" Name Found. {q}")
        name_in_data["dup_record_question"] = q

    db_name = Name(**name_in_data)
    db.add(db_name)
    db.commit()
    db.refresh(db_name)
    return db_name


def admin_get_name(db: Session, name_id: int) -> Name:
    return db.query(Name).filter(Name.id == name_id).first()


def admin_get_names(db: Session, skip: int = 0, limit: int = 100) -> list[Name]:
    return db.query(Name).offset(skip).limit(limit).all()


# can't get this working yet
def get_name_data(
    db: Session,
    first_name: str,
    last_name: str,
    dup_record_answer: Optional[str] = None,
) -> list[Name]:
    matches = (
        db.query(Name)
        .filter(
            and_(
                Name.first_name.ilike(first_name),
                Name.last_name.ilike(last_name),
            )
        )
        .all()
    )

    if not matches:
        return None

    if len(matches) > 1:
        if not dup_record_answer:
            q = "What is the full name of your city of residence?"
            raise HTTPException(status_code=400, detail=f" Name Found. {q}")
        matches = [
            m
            for m in matches
            if isinstance(m.dup_record_answer, str)
            and m.dup_record_answer.strip().lower() == dup_record_answer.strip().lower()
        ]
        if not matches:
            raise HTTPException(status_code=404, detail="No matching record found")

    return matches


def admin_update_name(db: Session, name_id: int, name_in: NameAdmin) -> Optional[Name]:
    db_name = admin_get_name(db, name_id)
    if not db_name:
        return None
    update_data = name_in.model_dump()
    if name_in.alternate_first_name:
        update_data["alternate_first_name"] = ",".join(name_in.alternate_first_name)
    if name_in.alternate_last_name:
        update_data["alternate_last_name"] = ",".join(name_in.alternate_last_name)

    for field, value in update_data.items():
        setattr(db_name, field, value)

    db.commit()
    db.refresh(db_name)
    return db_name


def update_name(db: Session, db_name: Name, name_in: NameUpdate) -> Optional[Name]:
    matches = (
        db.query(Name)
        .filter(
            and_(
                Name.first_name.ilike(name_in.first_name),
                Name.last_name.ilike(name_in.last_name),
            )
        )
        .all()
    )

    if not matches:
        return None

    if len(matches) > 1:
        if not name_in.dup_record_answer:
            q = "What is the full name of your city of residence?"
            raise HTTPException(status_code=400, detail=f" Name Found. {q}")
        match = next(
            (m for m in matches if m.dup_record_answer == name_in.dup_record_answer),
            None,
        )
        if not match:
            return None
        db_name = match
    else:
        db_name = matches[0]

    for (
        field,
        value,
    ) in name_in.model_dump().items():
        setattr(db_name, field, value)

    db.commit()
    db.refresh(db_name)
    return db_name


def admin_delete_name(db: Session, name_id: int) -> Optional[Name]:
    db_name = db.query(Name).filter(Name.id == name_id).first()
    if db_name:
        db.delete(db_name)
        db.commit()
    return db_name
