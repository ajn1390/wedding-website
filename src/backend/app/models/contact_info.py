from typing import Optional

from pydantic import BaseModel, EmailStr


class ContactInfoBase(BaseModel):
    email: EmailStr
    country_code: Optional[str]
    cell_number: Optional[str]


class ContactInfoCreate(ContactInfoBase):
    pass


class ContactInfoRead(ContactInfoBase):
    guest_id: int

    model_config = {"from_attributes": True}
