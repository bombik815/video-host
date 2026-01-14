import datetime
from typing import Annotated

from annotated_types import Len, MaxLen
from fastapi import Form
from pydantic import BaseModel

DescriptionString = Annotated[
    str,
    MaxLen(200),
]


class MovieBase(BaseModel):
    title: str
    description: DescriptionString = ""
    year: int


class MovieCreate(MovieBase):
    """
    Модель создания фильма
    """

    title: Annotated[str, Len(min_length=3, max_length=100)]
    description: DescriptionString
    year: Annotated[int, Form(min_value=1900, max_value=datetime.date.today().year)]
    slug: str


class MovieUpdate(MovieBase):
    """
    Модель для обновления информации о фильме
    """

    description: DescriptionString


class MovieUpdatePartial(BaseModel):
    title: str | None = None
    description: DescriptionString | None = None
    year: int | None = None


class Movie(MovieBase):
    """
    Модель фильма
    """

    slug: str
