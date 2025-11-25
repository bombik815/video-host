from typing import Annotated

from fastapi import (
    Depends,
    APIRouter,
    status,
)

from .crud import storage
from schemas.movie import Movie, MovieCreate
from .dependencies import get_movie_by_slug

router = APIRouter(prefix="/movies", tags=["Movies"])


"""
Возвращает список фильмов

Возвращает:
    list[Movie]: список объектов фильмов

"""


@router.get("/", response_model=list[Movie])
def get_movies() -> list[Movie]:
    return storage.get()


@router.post("/", response_model=Movie, status_code=status.HTTP_201_CREATED)
def creat_movie(
    movie_create: MovieCreate,
):
    return storage.create(movie_create)


"""
Возвращает объект фильма по его slug

Параметры:
    movie_slug (str): slug фильма

Возвращает:
    Movie: объект фильма

Исключения:
    HTTPException: 404 если фильм не найден
"""


@router.get("/{movie_slug}", response_model=Movie)
def get_movie(movie: Annotated[Movie, Depends(get_movie_by_slug)]) -> Movie:
    return movie
