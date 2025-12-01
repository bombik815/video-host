from fastapi import (
    status,
    APIRouter,
)

from api.api_v1.movies.crud import storage

from schemas.movie import Movie, MovieCreate


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
