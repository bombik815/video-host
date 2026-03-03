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

from core.config import API_TOKENS, USERS_DB
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


def api_token_required_for_unsafe_methods(
    request: Request,
    api_token: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(static_api_token),
    ] = None,
):
    """
    Проверяет наличие и действительность токена API для небезопасных методов HTTP.

    Эта функция служит зависимостью FastAPI и применяется к маршрутам,
    которые могут изменять данные (POST, PUT, PATCH, DELETE).
    Для безопасных методов (GET, HEAD, OPTIONS) проверка не требуется.

    Параметры:
        request (Request): Объект HTTP-запроса от FastAPI
        api_token (HTTPAuthorizationCredentials | None): Токен API из заголовка Authorization

    Исключения:
        HTTPException: 401 Unauthorized если токен не предоставлен
        HTTPException: 403 Forbidden если токен недействителен
    """
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


def user_basic_auth_required_for_unsafe_methods(
    request: Request,
    credentials: Annotated[
        HTTPBasicCredentials | None,
        Depends(user_basic_auth),
    ] = None,
):
    """
    Проверяет учетные данные пользователя по методу Basic Authentication.

    Эта функция служит зависимостью FastAPI и применяется к маршрутам,
    требующим аутентификации пользователя по логину и паролю.
    Сравнивает предоставленные учетные данные с базой пользователей.

    Параметры:
        credentials (HTTPBasicCredentials | None): Учетные данные пользователя из заголовка Authorization

    Исключения:
        HTTPException: 401 Unauthorized если учетные данные не предоставлены или неверны
    """

    if request.method not in UNSAFE_METHODS:
        return

    # Проверяем, что учетные данные были предоставлены
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User credentials required. Invalid username or password.",
            headers={"WWW-Authenticate": "Basic"},
        )

    # Проверяем, что предоставленные учетные данные являются действительными
    if (
        credentials
        and credentials.username in USERS_DB
        and USERS_DB[credentials.username] == credentials.password
    ):
        return

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="User credentials required. Invalid username or password.",
        headers={"WWW-Authenticate": "Basic"},
    )
