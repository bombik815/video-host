from fastapi import HTTPException
from starlette import status

from schemas.short_url import ShortUrl

from .crud import SHORT_URLS


"""
Возвращает объект сокращенной ссылки по ее slug

Parameters:
    slug (str): slug сокращенной ссылки

Returns:
    ShortUrl: объект сокращенной ссылки

Raises:
    HTTPException: 404 если сокращенная ссылка не найдена
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
