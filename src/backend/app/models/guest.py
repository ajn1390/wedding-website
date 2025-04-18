"""
Guest model.
"""

from __future__ import annotations

from pydantic import BaseModel, Field

from src.backend.app.models.contact_info import ContactInfoCreate, ContactInfoRead


class GuestBase(BaseModel):
    first_name: str = Field(...)
    last_name: str = Field(...)

    # model_config = {"from_attributes": True}


class GuestCreate(GuestBase):
    id: int
    is_primary: bool
    contact: ContactInfoCreate


class GuestRead(GuestBase):
    id: int
    is_primary: bool
    contact: ContactInfoRead

    model_config = {"from_attributes": True}
