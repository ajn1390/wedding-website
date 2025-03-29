"""
Name model.
"""

from typing import Optional

from src.backend.app.models.base import AppBaseModel


class NameBase(AppBaseModel):
    """
    Base class for Name objects. Don't return ID.
    """

    first_name: str
    last_name: str
    alternate_first_name: Optional[str] = None
    alternate_last_name: Optional[str] = None


class NameCreate(NameBase):
    """
    Create model for Name objects.
    """

    pass


class NameUpdate(AppBaseModel):
    """
    Base class for Name objects.
    """

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    alternate_first_name: Optional[str] = None
    alternate_last_name: Optional[str] = None


class ReadName(NameBase):
    class Config:
        orm_mode = True
