from typing import Annotated

from fastapi import (
    Depends,
    APIRouter,
)
from starlette import status

from api.api_v1.movies.crud import storage
from api.api_v1.movies.dependencies import get_movie_by_slug

from schemas.movie import Movie, MovieCreate

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

"""
Возвращает объект фильма по его slug

Параметры:
    movie_slug (str): slug фильма

Возвращает:
    Movie: объект фильма

Исключения:
    HTTPException: 404 если фильм не найден
"""


@router.get("/", response_model=Movie)
def get_movie(movie: Annotated[Movie, Depends(get_movie_by_slug)]) -> Movie:
    return movie


"""
Удаляет объект фильма по его slug

Параметры:
    movie_slug (str): slug фильма

Возвращает:
    None: тело пустое

Исключения:
    HTTPException: 404 если фильм не найден (проверка выполняется в зависимости)
"""


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_movie(movie: Annotated[Movie, Depends(get_movie_by_slug)]) -> None:
    storage.delete(movie=movie)
