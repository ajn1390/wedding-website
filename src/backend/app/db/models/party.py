"""
Database storage model for Party objects.
Parties are groups of one to two Guests
"""
# import uuid

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.backend.app.db.base_class import Base


class Party(Base):
    __tablename__ = "parties"

    id = Column(Integer, primary_key=True)
    label = Column(String, index=True, nullable=False)
    primary_guest_id = Column(
        Integer, ForeignKey("guests.id"), nullable=False, unique=True
    )
    secondary_guest_id = Column(
        Integer, ForeignKey("guests.id"), nullable=True, unique=True
    )

    primary_guest = relationship("Guest", foreign_keys=[primary_guest_id])
    secondary_guest = relationship("Guest", foreign_keys=[secondary_guest_id])
