from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from src.backend.app.db.models.contact_info import ContactInfo
from src.backend.app.db.models.guest import Guest
from src.backend.app.db.models.party import Party
from src.backend.app.models.guest import GuestCreate


def guest_email_exists(db: Session, email: str) -> bool:
    # return db.query(ContactInfo).filter(ContactInfo.email == email).first() is not None

    stmt = select(ContactInfo).where(ContactInfo.email == email)
    result = db.execute(stmt).first()
    return result is not None


def get_guest_by_email(db: Session, email: str) -> Guest | None:
    contact = db.query(ContactInfo).filter(ContactInfo.email == email).first()
    return contact.guest if contact else None


def delete_guest_info(db: Session, id: int) -> Guest | None:
    guest = db.query(Guest).filter(Guest.id == id).first()
    if not guest:
        return None

    # if guest.contact_info:
    #     db.delete(guest.contact_info)

    db.delete(guest)
    db.commit()
    return guest


def get_party_by_guest_id(db: Session, guest_id: int) -> Party | None:
    print("GUEST ID", guest_id)
    return (
        db.query(Party)
        .filter(
            or_(
                Party.primary_guest_id == guest_id, Party.secondary_guest_id == guest_id
            )
        )
        .first()
    )


def guest_create(db: Session, guest_data: GuestCreate) -> Guest:
    new_guest = Guest(
        first_name=guest_data.first_name,
        last_name=guest_data.last_name,
        is_primary=guest_data.is_primary,
    )

    db.add(new_guest)
    # db.commit()
    # db.refresh(new_guest)
    db.flush()  # Assign id to Guest obj without committing

    contact = ContactInfo(
        guest_id=new_guest.id,
        email=guest_data.contact.email,
        country_code=guest_data.contact.country_code,
        cell_number=guest_data.contact.cell_number,
    )

    db.add(contact)
    db.commit()
    db.refresh(new_guest)  # need?

    return new_guest


def create_party_from_primary_guest(db: Session, guest: Guest) -> Party:
    party = Party(primary_guest_id=guest.id, label=guest.last_name)
    db.add(party)
    db.commit()
    db.refresh(party)
    return party


def assign_secondary_guest_to_party(
    db: Session, primary_email: str, secondary_guest_id: int
) -> Party:
    primary_guest = get_guest_by_email(db, primary_email)
    if not primary_guest:
        raise ValueError("Guest not found")
    party = db.query(Party).filter(Party.primary_guest_id == primary_guest.id).first()

    if not party:
        raise ValueError("Party not found for primary guest")

    # if party.secondary_guest_id:
    #     raise ValueError("Secondary guest already assigned")

    party.secondary_guest_id = secondary_guest_id
    db.commit()
    db.refresh(party)
    return party


def get_contact_info_by_id(db: Session, id: int) -> ContactInfo | None:
    guest = db.query(Guest).filter(Guest.id == id).first()
    if not guest:
        return None
    return guest.contact


def get_all_guest_data_by_id(db: Session, id: int) -> Guest | None:
    return db.query(Guest).filter(Guest.id == id).first()
