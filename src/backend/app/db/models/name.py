"""
Database storage model for Name objects.
"""
# import uuid

import sqlalchemy as sa

from src.backend.app.db.base_class import Base


class Name(Base):
    """
    Database storage model for Name objects.
    """

    # __tablename__ = "names"

    id = sa.Column(sa.Integer, primary_key=True)
    # uid = sa.Column(GUID, unique=True, index=True, default=uuid.uuid4)
    first_name = sa.Column(sa.String, index=True, nullable=False)
    last_name = sa.Column(sa.String, index=True, nullable=False)
    alternate_first_name = sa.Column(sa.String, index=True)
    altnerate_last_name = sa.Column(sa.String, index=True)
