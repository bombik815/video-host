from fastapi import (
    status,
    APIRouter,
    BackgroundTasks,
    Depends,
)

from api.api_v1.movies.crud import storage
from api.api_v1.movies.dependencies import save_storage_state

from schemas.movie import Movie, MovieCreate, MovieRead

router = APIRouter(
    prefix="/movies",
    tags=["Movies"],
    dependencies=[Depends(save_storage_state)],
)

"""
Возвращает список фильмов

Возвращает:
    list[Movie]: список объектов фильмов

"""


@router.get("/", response_model=list[MovieRead])
def get_movies() -> list[Movie]:
    return storage.get()


@router.post("/", response_model=Movie, status_code=status.HTTP_201_CREATED)
def create_movie(movie_create: MovieCreate, background_tasks: BackgroundTasks):
    return storage.create(movie_create)
