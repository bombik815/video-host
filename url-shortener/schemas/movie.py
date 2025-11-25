import datetime
import random
from typing import Annotated

from annotated_types import Len
from fastapi import Form
from pydantic import BaseModel, Field


class MovieBase(BaseModel):
    title: str
    description: str
    year: int


class MovieCreate(MovieBase):
    """
    Модель создания фильма
    """

    title: Annotated[str, Len(min_length=3, max_length=100)]
    description: Annotated[str, Len(min_length=3, max_length=100)]
    year: Annotated[int, Form(min_value=1900, max_value=datetime.date.today().year)]


class Movie(MovieBase):
    """
    Модель фильма
    """

    id: int = Field(default_factory=lambda: random.randint(1_000_000, 9_999_999))
