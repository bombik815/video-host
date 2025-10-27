from fastapi import HTTPException
from starlette import status

from .crud import MOVIES

from schemas.movie import Movie


"""
Возвращает объект фильма по его ID

Параметры:
    movie_id (int): ID фильма

Возвращает:
    Movie: объект фильма

Исключения:
    HTTPException: 404 если фильм не найден
"""


def get_movie_by_id(movie_id: int) -> Movie:

    movie: Movie | None = next(
        (movie for movie in MOVIES if movie.id == movie_id),
        None,
    )
    if movie:
        return movie

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Movie with ID {movie_id} not found",
    )
