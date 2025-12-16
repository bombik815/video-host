import datetime
from typing import Annotated

from annotated_types import Len, MaxLen
from fastapi import Form
from pydantic import BaseModel


class MovieBase(BaseModel):
    title: str
    description: Annotated[
        str,
        MaxLen(200),
    ] = ""
    year: int


class MovieCreate(MovieBase):
    """
    Модель создания фильма
    """

    title: Annotated[str, Len(min_length=3, max_length=100)]
    description: Annotated[str, Len(min_length=3, max_length=100)]
    year: Annotated[int, Form(min_value=1900, max_value=datetime.date.today().year)]
    slug: str


class MovieUpdate(MovieBase):
    """
    Модель для обновления информации о фильме
    """
    description: Annotated[str, Len(min_length=3, max_length=100)]


class Movie(MovieBase):
    """
    Модель фильма
    """

    slug: str
