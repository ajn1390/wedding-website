from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from src.backend.app.api.utils.storage import get_db
from src.backend.app.db.crud.crud import (
    assign_secondary_guest_to_party,
    create_party_from_primary_guest,
    delete_guest_info,
    get_all_guest_data_by_id,
    get_contact_info_by_id,
    get_guest_by_email,
    get_party_by_guest_id,
    guest_create,
    guest_email_exists,
)
from src.backend.app.db.database import init_db
from src.backend.app.db.models.party import Party
from src.backend.app.models.contact_info import ContactInfoBase
from src.backend.app.models.guest import GuestCreate, GuestRead
from src.backend.app.models.party import PartyRead

router = APIRouter()

init_db()


@router.post("/guests/", response_model=GuestRead)
async def create_guest(guest_data: GuestCreate, db: Session = Depends(get_db)):
    if guest_email_exists(db, guest_data.contact.email):
        raise HTTPException(
            status_code=404,
            detail=f"Guest email {guest_data.contact.email} already exists",
        )

    new_guest = guest_create(db, guest_data)

    if new_guest.is_primary:
        create_party_from_primary_guest(db, new_guest)

    return new_guest


@router.get("/guests/{guest_id}", response_model=GuestRead)
async def read_guest_by_id(guest_id: int, db: Session = Depends(get_db)):
    guest = get_all_guest_data_by_id(db, guest_id)
    if guest is None:
        raise HTTPException(status_code=404, detail=f"Guest {guest_id} not found")
    return guest


@router.get("/guests/by-email/{email}", response_model=GuestRead)
async def admin_guest_by_email(email: str, db: Session = Depends(get_db)):
    guest = get_guest_by_email(db, email)
    if not guest:
        raise HTTPException(
            status_code=404, detail=f"No guest found with email {email}"
        )
    return guest


@router.delete("guests/{guest_id}", response_model=GuestRead)
async def delete_guest(guest_id: int, db: Session = Depends(get_db)):
    guest = delete_guest_info(db, guest_id)
    if guest is None:
        raise HTTPException(status_code=404, detail=f"Guest {guest_id} not found")
    return guest


def party_guests(party: Party) -> PartyRead:
    party_guests = []
    if party.primary_guest:
        party_guests.append(party.primary_guest)
    if party.secondary_guest:
        party_guests.append(party.secondary_guest)

    return PartyRead(label=party.label, id=party.id, guests=party_guests)


@router.post("/parties/assign-secondary/")
async def assign_secondary_guest(
    primary_email: str = Body(..., embed=True),
    secondary_guest_id: int = Body(..., embed=True),
    db: Session = Depends(get_db),
):
    try:
        party = assign_secondary_guest_to_party(
            db=db, primary_email=primary_email, secondary_guest_id=secondary_guest_id
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return party_guests(party)


@router.get("/parties/by-email/{email}", response_model=PartyRead)
async def get_party_guests_by_email(email: str, db: Session = Depends(get_db)):
    guest = get_guest_by_email(db, email)
    if not guest:
        raise HTTPException(
            status_code=404, detail=f"No guest found with email {email}"
        )
    party = get_party_by_guest_id(db, guest.id)
    print("GUEST", guest.id, "PARTY", party)
    if not party:
        raise HTTPException(status_code=404, detail="No party found for guest")

    return party_guests(party)


@router.get("/guests/{guest_id}/contact-info", response_model=ContactInfoBase)
async def read_contact_by_id(guest_id: int, db: Session = Depends(get_db)):
    contact_info = get_contact_info_by_id(db, guest_id)
    if not contact_info:
        raise HTTPException(
            status_code=404, detail=f"No contact info found for guest {guest_id}"
        )
    return contact_info
