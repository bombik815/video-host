from typing import Annotated

from fastapi import (
    Depends,
    APIRouter,
    BackgroundTasks,
)
from starlette import status

from api.api_v1.movies.crud import storage
from api.api_v1.movies.dependencies import get_movie_by_slug

from schemas.movie import Movie, MovieRead, MovieUpdate, MovieUpdatePartial

router = APIRouter(
    prefix="/{slug}",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Movie not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Movie with slug <slug> not found"}
                }
            },
        }
    },
)

MovieDep = Annotated[Movie, Depends(get_movie_by_slug)]


@router.get("/", response_model=MovieRead)
def get_movie(movie: MovieDep) -> Movie:
    """
    Получить фильм по его slug.

    - **slug**: строковый идентификатор фильма
    - Возвращает объект фильма
    - Выбрасывает 404, если фильм не найден
    """
    return movie


@router.put("/", response_model=Movie)
def update_movie_details(
    movie: MovieDep,
    movie_in: MovieUpdate,
    background_tasks: BackgroundTasks,
):
    """
    Обновить информацию о фильме по его slug.

    - **slug**: строковый идентификатор фильма (из пути)
    - **movie_in**: обновленная информация о фильме
    - Возвращает обновленный объект фильма
    - Выбрасывает 404, если фильм не найден
    """
    background_tasks.add_task(storage.save_state)
    return storage.update(
        movie=movie,
        movie_in=movie_in,
    )


@router.patch("/", response_model=Movie)
def update_movie_details_partial(
    movie: MovieDep,
    movie_in: MovieUpdatePartial,
    background_tasks: BackgroundTasks,
) -> Movie:
    background_tasks.add_task(storage.save_state)
    return storage.update_partial(
        movie=movie,
        movie_in=movie_in,
    )


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_movie(movie: MovieDep, background_tasks: BackgroundTasks) -> None:
    """
    Удалить фильм по его slug.

    - **slug**: строковый идентификатор фильма
    - В случае успеха возвращает статус 204 (No Content)
    - Выбрасывает 404, если фильм не найден
    """
    background_tasks.add_task(storage.save_state)
    storage.delete(movie=movie)
