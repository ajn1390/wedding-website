"""
Database storage model for Name objects.
"""
# import uuid

import sqlalchemy as sa

from app.db.base_class import Base
# from app.db.types import GUID


class Name(Base):
    """
    Database storage model for Name objects.
    """

    __tablename__ = 'names'

    id = sa.Column(sa.Integer, primary_key=True)
    # uid = sa.Column(GUID, unique=True, index=True, default=uuid.uuid4)
    first = sa.Column(sa.String, index=True, nullable=False)
    last = sa.Column(sa.String, index=True, nullable=False)
    alternate_first = sa.Column(sa.String, index=True)
    altnerate_last = sa.Column(sa.String, index=True)