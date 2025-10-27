from typing import Annotated

from fastapi import Depends, APIRouter

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
