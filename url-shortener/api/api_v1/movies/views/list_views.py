from fastapi import (
    status,
    APIRouter,
    BackgroundTasks,
)

from api.api_v1.movies.crud import storage

from schemas.movie import Movie, MovieCreate, MovieRead

router = APIRouter(prefix="/movies", tags=["Movies"])

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
    background_tasks.add_task(storage.save_state)  # Добавим задачу на сохранение данных
    return storage.create(movie_create)
