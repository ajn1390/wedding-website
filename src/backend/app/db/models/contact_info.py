"""
Database storage model for ContactInfo objects.
"""
# import uuid

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.backend.app.db.base_class import Base


class ContactInfo(Base):
    guest_id = Column(Integer, ForeignKey("guests.id"), primary_key=True)
    email = Column(String, nullable=False, index=True, unique=True)
    country_code = Column(String, nullable=True)  # sometimes gets added with '+' etc
    cell_number = Column(String, nullable=True)  # sometimes gets added with '-' etc

    guest = relationship("Guest", back_populates="contact", uselist=False)
