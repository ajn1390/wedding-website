"""
Name model.
"""
from typing import Optional
# from uuid import UUID

from app.models.base import AppBaseModel


class NameBase(AppBaseModel):
    """
    Base class for Name objects.
    """
    first: str
    last: str
    alternate_first: Optional[str] = None
    altnerate_last: Optional[str] = None


class NameCreate(NameBase):
    """
    Create model for Name objects.
    """
    pass