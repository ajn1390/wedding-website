"""
Customized declarative base model for SQLAlchemy.
"""

from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base, declared_attr

from src.backend.app.utils.strutils import camel_to_snake


class CustomBase(object):
    """
    Customized declarative base with correct table-naming conventions.
    Used for ORM models (object relational mapping system) which handle the
    conversion between Python objects and database records.
    The declared_attr decorator means that when we make a new ORM model inherting
    from CustomBase, SQLA will call this method to compute the attr once.

    Automatically creates table name from model class so UserName -> user_names
    """

    @declared_attr
    def __tablename__(cls) -> str:
        return camel_to_snake(cls.__name__) + "s"


# Objects
metadata = MetaData()  # creates a container for db schema
Base = declarative_base(cls=CustomBase, metadata=metadata)
