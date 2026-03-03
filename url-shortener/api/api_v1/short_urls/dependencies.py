import logging
from typing import Annotated

from fastapi import (
    HTTPException,
    BackgroundTasks,
    Request,
    status,
    Depends,
)
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from core.config import API_TOKENS
from schemas.short_url import ShortUrl

from .crud import storage

log = logging.getLogger(__name__)


UNSAFE_METHODS = frozenset(
    {
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
    }
)

static_api_token = HTTPBearer(
    scheme_name="Static API token",
    description="Your Static API token from the developer portal",
    auto_error=False,
)


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


def save_storage_state(request: Request, background_tasks: BackgroundTasks):
    yield
    if request.method in UNSAFE_METHODS:
        log.info("Add background task to save storage.")
        background_tasks.add_task(storage.save_state)


def api_token_required_for_unsafe_methods(
    request: Request,
    api_token: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(static_api_token),
    ] = None,
):
    log.info("API token: %s", api_token)
    # Require token only for unsafe methods; allow safe methods without token
    if request.method not in UNSAFE_METHODS:
        return

    # Проверяем, что токен API был предоставлен
    if not api_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API token is required",
        )

    # Проверяем, что предоставленный токен API является действительным
    if api_token.credentials not in API_TOKENS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API token",
        )
