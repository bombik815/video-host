from typing import Annotated

from fastapi import (
    Depends,
    APIRouter,
)
from starlette import status

from api.api_v1.movies.crud import storage
from api.api_v1.movies.dependencies import (
    get_movie_by_slug,
    api_token_required,
)

from schemas.movie import (
    Movie,
    MovieRead,
    MovieUpdate,
    MovieUpdatePartial,
)

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
    _=Depends(api_token_required),
):
    """
    Обновить информацию о фильме по его slug.

    - **slug**: строковый идентификатор фильма (из пути)
    - **movie_in**: обновленная информация о фильме
    - Возвращает обновленный объект фильма
    - Выбрасывает 404, если фильм не найден
    """
    return storage.update(
        movie=movie,
        movie_in=movie_in,
    )


@router.patch("/", response_model=Movie)
def update_movie_details_partial(
    movie: MovieDep,
    movie_in: MovieUpdatePartial,
    _=Depends(api_token_required),
) -> Movie:
    return storage.update_partial(
        movie=movie,
        movie_in=movie_in,
    )


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(
    movie: MovieDep,
    _=Depends(api_token_required),
) -> None:
    """
    Удалить фильм по его slug.

    - **slug**: строковый идентификатор фильма
    - В случае успеха возвращает статус 204 (No Content)
    - Выбрасывает 404, если фильм не найден
    """
    storage.delete(movie=movie)
