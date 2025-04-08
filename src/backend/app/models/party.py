from typing import Optional

from pydantic import BaseModel

from backend.app.models.guest import GuestRead


class PartyBase(BaseModel):
    label: str

    model_config = {"from_attributes": True}


class PartyCreate(PartyBase):
    primary_guest_id = int
    secondary_guest_id = Optional[int] = None


class PartyRead(PartyBase):
    id: int
    guests: list[GuestRead]
