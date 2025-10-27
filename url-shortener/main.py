from typing import Annotated

from fastapi import FastAPI, Request, HTTPException, status, Depends

from api import router as api_router
from api.redirect_views import router as redirect_views

from schemas.movie import Movie

# Константы
# Список фильмов
MOVIES = [
    Movie(
        id=1,
        title="Крестный отец",
        description="Криминальная драма о семье мафиози Корлеоне",
        year=1972,
    ),
    Movie(
        id=2,
        title="Побег из Шоушенка",
        description="Драма о несправедливо осужденном банкире",
        year=1994,
    ),
    Movie(
        id=3,
        title="Темный рыцарь",
        description="Бэтмен сражается с Джокером",
        year=2008,
    ),
]

app = FastAPI(
    title="URL Shortener",
    description="URL Shortener",
)

app.include_router(redirect_views)
app.include_router(api_router)


@app.get("/")
async def read_root(
    request: Request,
    name: str = "Shortener",
):
    """
    Корневой view - возвращает JSON со ссылками на документацию
    """
    docs_url = request.url.replace(
        path="/docs",
        query="",
    )
    redoc_url = request.url.replace(
        path="/redoc",
        query="",
    )

    return {
        "message": f"Welcome to the URL {name} API",
        "docs": str(docs_url),
        "redoc": str(redoc_url),
    }


@app.get(
    "/movies/",
    response_model=list[Movie],
)
def get_movies() -> list[Movie]:
    return MOVIES


"""
Возвращает фильм по его ID

Parameters:
    movie_id (int): идентификатор фильма

Returns:
    Movie: объект фильма

Raises:
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


@app.get(
    "/movies/{movie_id}",
    response_model=Movie,
)
def get_movie(
    movie: Annotated[
        Movie,
        Depends(get_movie_by_id),
    ],
) -> Movie:

    return movie
