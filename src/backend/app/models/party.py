from pydantic import BaseModel

from src.backend.app.models.guest import GuestRead


class PartyBase(BaseModel):
    id: int
    label: str

    # model_config = {"from_attributes": True}


class PartyCreate(PartyBase):
    primary_guest_id: int
    secondary_guest_id: int | None = None


class PartyRead(PartyBase):
    # id: int
    # label: str
    guests: list[GuestRead]
    model_config = {"from_attributes": True}
