from typing import Annotated

from fastapi import (
    Depends,
    APIRouter,
)
from starlette import status

from api.api_v1.movies.crud import storage
from api.api_v1.movies.dependencies import get_movie_by_slug

from schemas.movie import Movie

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


@router.get("/", response_model=Movie)
def get_movie(movie: Annotated[Movie, Depends(get_movie_by_slug)]) -> Movie:
    """
    Получить фильм по его slug.

    - **slug**: строковый идентификатор фильма
    - Возвращает объект фильма
    - Выбрасывает 404, если фильм не найден
    """
    return movie


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_movie(movie: Annotated[Movie, Depends(get_movie_by_slug)]) -> None:
    """
    Удалить фильм по его slug.

    - **slug**: строковый идентификатор фильма
    - В случае успеха возвращает статус 204 (No Content)
    - Выбрасывает 404, если фильм не найден
    """
    storage.delete(movie=movie)
