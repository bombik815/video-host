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
    HTTPBasic,
    HTTPBasicCredentials,
)

from core.config import USERS_DB
from schemas.short_url import ShortUrl

from api.api_v1.auth.services import (
    redis_tokens,
    redis_users,
)
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

user_basic_auth = HTTPBasic(
    scheme_name="Basic Auth",
    description="Your Basic Auth token from the developer portal",
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


def validate_api_token(api_token: HTTPAuthorizationCredentials):
    # Проверяет, что предоставленный API токен содержится в наборе допустимых токенов в REDIS
    if redis_tokens.token_exist(api_token.credentials):
        return
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Invalid API token",
    )


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
    validate_api_token(api_token=api_token)


def validate_basic_auth(
    credentials: HTTPBasicCredentials | None,
):
    # Проверяем, что предоставленные учетные данные являются действительными в REDIS БД
    if credentials and redis_users.validate_user_password(
        username=credentials.username,
        password=credentials.password,
    ):
        return
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password.",
        headers={"WWW-Authenticate": "Basic"},
    )


def user_basic_auth_required_for_unsafe_methods(
    request: Request,
    credentials: Annotated[
        HTTPBasicCredentials | None,
        Depends(user_basic_auth),
    ] = None,
):
    if request.method not in UNSAFE_METHODS:
        return
    validate_basic_auth(credentials=credentials)


def api_token_or_user_basic_auth_required_for_unsafe_methods(
    request: Request,
    api_token: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(static_api_token),
    ] = None,
    credentials: Annotated[
        HTTPBasicCredentials | None,
        Depends(user_basic_auth),
    ] = None,
):
    """
    Проверяет, что для не безопасных HTTP методов (например, POST, PUT, DELETE)
    предоставлен либо API токен, либо базовая авторизация (логин и пароль).
    Если ни одно из этих условий не выполнено, вызывает исключение с кодом 401 Unauthorized.
    """
    if request.method not in UNSAFE_METHODS:
        return
    # проверяем если логин и пароль используется
    if credentials:
        return validate_basic_auth(credentials=credentials)
    # Проверяем если токен  используется
    if api_token:
        return validate_api_token(api_token=api_token)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="API token or basic auth required!",
    )
