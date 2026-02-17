import logging

from fastapi import (
    HTTPException,
    status,
    BackgroundTasks,
    Request,
)

from .crud import storage

from schemas.movie import Movie

log = logging.getLogger(__name__)


UNSAFE_METHODS = frozenset(
    {
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
    }
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


def get_movie_by_slug(movie_slug: str) -> Movie:

    movie: Movie | None = storage.get_by_slug(movie_slug)
    if movie:
        return movie

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Movie with slug {movie_slug} not found",
    )


def save_storage_state(request: Request, background_tasks: BackgroundTasks):
    yield
    if request.method in UNSAFE_METHODS:
        log.info("Add background task to save storage.")
        background_tasks.add_task(storage.save_state)
