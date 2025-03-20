"""
Base model class.
"""
import typing as tp

import orjson
from pydantic import BaseModel


def orjson_dumps(v: tp.Any, *, default: tp.Optional[tp.Callable]) -> str:
    """Convert the returned bytes back to string."""
    return orjson.dumps(v, default=default).decode()


class AppBaseModel(BaseModel):
    """
    Base model class for application models.
    """

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps

