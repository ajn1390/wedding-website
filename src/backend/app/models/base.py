"""
App Base model class. Maybe this should be called schemas?
Do I even need this orjson?
"""

import typing as tp

import orjson
from pydantic import BaseModel


def orjson_dumps(v: tp.Any, *, default: tp.Optional[tp.Callable]) -> str:
    """Convert the returned bytes back to string."""
    return orjson.dumps(v, default=default).decode()


# do I really need this?
class AppBaseModel(BaseModel):
    """
    Base model class for application models.
    This will override and use our implementation of parsing objects to JSON
    """

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
