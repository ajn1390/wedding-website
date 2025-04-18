# """
# Name model.
# """

# from typing import Optional

# from pydantic import BaseModel, Field


# class NameBase(BaseModel):
#     """
#     Base class for Name objects. Don't return ID.
#     """

#     first_name: str = Field(...)
#     last_name: str = Field(...)
#     # alternate_first_name: Optional[str] = None
#     # alternate_last_name: Optional[str] = None
#     # dup_record_question = Optional[str] = None
#     # dup_record_answer = Optional[str] = None


# class NameCreate(NameBase):
#     """
#     Create model for Name objects.
#     """

#     dup_record_answer = Optional[str] = None

#     pass


# class NameAdmin(NameCreate):
#     id: int
#     alternate_first_name: Optional[list[str]] = None
#     alternate_last_name: Optional[list[str]] = None
#     dup_record_question = Optional[str] = None
#     dup_record_answer = Optional[str] = None

#     model_config = {"from_attributes": True}


# class NameUpdate(NameBase):
#     """
#     Base class for Name objects.
#     """

#     dup_record_answer = Optional[str] = None

#     pass


# class NameOut(NameBase):
#     model_config = {"from_attributes": True}
