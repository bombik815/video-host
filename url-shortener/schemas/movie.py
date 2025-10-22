from pydantic import BaseModel


class MovieBase(BaseModel):
    title: str
    description: str
    year: int


class Movie(MovieBase):
    """
    Модель фильма
    """
    id: int
