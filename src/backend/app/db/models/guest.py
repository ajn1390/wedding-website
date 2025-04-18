"""
Database storage model for Guest objects.
"""
# import uuid

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from src.backend.app.db.base_class import Base


class Guest(Base):
    __tablename__ = "guests"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, index=True, nullable=False)
    last_name = Column(String, index=True, nullable=False)
    is_primary = Column(Boolean, default=False, nullable=False)

    contact = relationship(
        "ContactInfo",
        back_populates="guest",
        uselist=False,
        cascade="all, delete-orphan",
    )
