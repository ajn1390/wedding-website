from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.backend.app.api.utils.storage import get_db
from src.backend.app.db.crud.name import (
    admin_create_name,
    admin_delete_name,
    admin_get_name,
    admin_get_names,
    admin_update_name,
    create_name,
    update_name,
)
from src.backend.app.db.database import init_db
from src.backend.app.models.name import NameAdmin, NameCreate, NameOut, NameUpdate

router = APIRouter()

init_db()

# not sure if the response model should be read name or name base but ok for now


@router.post("/names/", response_model=NameOut)
async def create_your_name(name_in: NameCreate, db: Session = Depends(get_db)):
    return create_name(db, name_in)


@router.post("/names/", response_model=list[NameOut])
async def read_your_names(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return admin_get_names(db, skip=skip, limit=limit)


@router.post("/names/{name_id}", response_model=NameOut)
async def read_your_name(name_id: int, db: Session = Depends(get_db)):
    name = admin_get_name(db, name_id)
    if not name:
        raise HTTPException(status_code=404, detail="Name not found")
    return name


@router.put("/names/{name_id}", response_model=NameOut)
async def update_your_name(
    name_id: int, name_in: NameUpdate, db: Session = Depends(get_db)
):
    name = admin_get_name(db, name_id)
    if not name:
        raise HTTPException(status_code=404, detail="Name not found")
    updated_name = update_name(db, name, name_in)
    return updated_name


@router.delete("/names/{name_id}", response_model=NameOut)
async def delete_your_name(name_id: int, db: Session = Depends(get_db)):
    name = admin_get_name(db, name_id)
    if not name:
        raise HTTPException(status_code=404, detail="Name not found")
    deleted_name = admin_delete_name(db, name)
    return deleted_name


##############


@router.post("/admin/names/", response_model=NameAdmin, response_class=JSONResponse)
async def admin_create_name_endpoint(
    name: NameAdmin, db: Session = Depends(get_db)
) -> JSONResponse:
    result = admin_create_name(db, name)
    return JSONResponse(
        content=NameAdmin.model_validate(result).model_dump(),
        headers={"X-Admin-Name-Created": "true"},
    )


@router.post("/names/", response_model=NameOut, response_class=JSONResponse)
async def create_name_endpoint(
    name: NameCreate, db: Session = Depends(get_db)
) -> JSONResponse:
    result = create_name(db=db, name=name)
    return JSONResponse(
        content=NameOut.model_validate(result).model_dump(),
        headers={"X-Name-Created": "true"},
    )


@router.get("/names/", response_model=list[NameOut], response_class=JSONResponse)
async def admin_get_names_endpoint(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> JSONResponse:
    result = admin_get_names(db=db, skip=skip, limit=limit)
    return JSONResponse(
        content=[NameOut.model_validate(r).model_dump() for r in result],
        headers={"X-Total-Count": str(len(result))},
    )


@router.get(
    "/admin/names/by-id/{name_id}",
    response_model=NameAdmin,
    response_class=JSONResponse,
)
async def admin_get_name_by_id_endpoint(
    name_id: int, db: Session = Depends(get_db)
) -> JSONResponse:
    db_name = admin_get_name(db, name_id)
    if db_name is None:
        raise HTTPException(status_code=404, detail="Name not found")
    return JSONResponse(
        content=NameAdmin.model_validate(db_name).model_dump(),
        headers={"X-Name-Fetched": "true"},
    )


@router.put("/names/", response_model=NameOut, response_class=JSONResponse)
async def update_name_endpoint(
    name: NameUpdate, db: Session = Depends(get_db)
) -> JSONResponse:
    updated_name = update_name(db, name)
    if updated_name is None:
        raise HTTPException(status_code=404, detail="Name not found")
    return JSONResponse(
        content=NameOut.model_validate(updated_name).model_dump(),
        headers={"X-Name-Updated": "true"},
    )


@router.put(
    "/admin/names/{name_id}", response_model=NameOut, response_class=JSONResponse
)
async def admin_update_name_endpoint(
    name_id: int, name: NameAdmin, db: Session = Depends(get_db)
) -> JSONResponse:
    updated_name = admin_update_name(db, name_id, name)
    if updated_name is None:
        raise HTTPException(status_code=404, detail="Name not found")
    return JSONResponse(
        content=NameOut.model_validate(updated_name).model_dump(),
        headers={"X-Admin-Name-Update": "true"},
    )


@router.delete("/admin/names/{name_id}", response_class=JSONResponse)
async def admin_delete_name_endpoint(
    name_id: int, db: Session = Depends(get_db)
) -> JSONResponse:
    deleted = admin_delete_name(db, name_id)
    if deleted is None:
        raise HTTPException(status_code=404, detail="Name not found")
    return JSONResponse(
        content={"ok": True, "message": "Deleted name"},
        headers={"X-Name-Deleted": "true"},
    )


@router.get(
    "/admin/names/", response_model=list[NameAdmin], response_class=JSONResponse
)
async def admin_get_name_names_endpoint(db: Session = Depends(get_db)) -> JSONResponse:
    result = admin_get_names(db=db)
    return JSONResponse(
        content=[NameAdmin.model_validate(r).model_dump() for r in result],
        headers={"X-Admin-Total": str(len(result))},
    )
