from typing import Annotated

from fastapi import FastAPI, Request, HTTPException, status, Depends


from schemas.short_url import ShortUrl
from schemas.movie import Movie
from fastapi.responses import RedirectResponse


# Константы
SHORT_URLS = [
    ShortUrl(
        target_url="https://example.com",
        slug="example",
    ),
    ShortUrl(
        target_url="https://google.com",
        slug="search",
    ),
]

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
    "/short-urls/",
    response_model=list[ShortUrl],
)
def read_short_urls_list():
    return SHORT_URLS


"""
Извлекает объект ShortUrl из списка SHORT_URLS по его slug.

Вызывает ошибку 404, если slug не найден.

Параметры:
    slug (str): идентификатор (slug) искомого ShortUrl

Возвращает:
    ShortUrl: найденный объект ShortUrl
"""


def prefetch_short_urls(slug: str) -> ShortUrl:

    url: ShortUrl | None = next(
        (url for url in SHORT_URLS if url.slug == slug),
        None,
    )
    if url:
        return url

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"URL {slug!r} not found",
    )


@app.get("/r/{slug}")
@app.get("/r/{slug}/")
def redirect_short_url(
    url: Annotated[
        ShortUrl,
        Depends(prefetch_short_urls),
    ],
):
    return RedirectResponse(url=url.target_url)


"""
Возвращает подробную информацию о сокращенной ссылке

Parameters:
    slug (str): slug сокращенной ссылки

Returns:
    ShortUrl: объект сокращенной ссылки
"""


@app.get(
    "/short-urls/{slug}/",
    response_model=ShortUrl,
)
def read_short_url_details(
    url: Annotated[
        ShortUrl,
        Depends(prefetch_short_urls),
    ],
) -> ShortUrl:
    return url


"""
Возвращает список всех фильмов, хранящихся в системе

Returns:
    list[Movie]: список фильмов
"""


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
