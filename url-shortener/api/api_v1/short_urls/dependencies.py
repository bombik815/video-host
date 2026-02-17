import logging

from fastapi import HTTPException, BackgroundTasks
from starlette import status

from schemas.short_url import ShortUrl

from .crud import storage

log = logging.getLogger(__name__)

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

    url: ShortUrl | None = storage.get_by_slug(slug=slug)
    if url:
        return url

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"URL {slug!r} not found",
    )


def save_storage_state(background_tasks: BackgroundTasks):
    yield
    log.info("Add background task to save storage.")
    background_tasks.add_task(storage.save_state)
