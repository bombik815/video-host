import datetime

from typing import Annotated

from annotated_types import Len

import status
from fastapi import (
    Depends,
    APIRouter,
    status,
    Form,
)

from .crud import MOVIES
from schemas.movie import Movie
from .dependencies import get_movie_by_id

router = APIRouter(prefix="/movies", tags=["Movies"])


"""
Возвращает список фильмов

Возвращает:
    list[Movie]: список объектов фильмов

"""


@router.get("/", response_model=list[Movie])
def get_movies() -> list[Movie]:
    return MOVIES


@router.post("/", response_model=Movie, status_code=status.HTTP_201_CREATED)
def creat_movie(
    title: Annotated[str, Form()],
    description: Annotated[str, Len(min_length=3, max_length=100), Form()],
    year: Annotated[int, Form(min_value=1900, max_value=datetime.date.today().year)],
):
    return Movie(title=title, description=description, year=year)


"""
Возвращает объект фильма по его ID

Параметры:
    movie_id (int): ID фильма

Возвращает:
    Movie: объект фильма

Исключения:
    HTTPException: 404 если фильм не найден
"""


@router.get("/{movie_id}", response_model=Movie)
def get_movie(movie: Annotated[Movie, Depends(get_movie_by_id)]) -> Movie:
    return movie
