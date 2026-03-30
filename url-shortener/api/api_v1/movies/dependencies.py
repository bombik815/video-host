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

from core.config import (
    USERS_DB,
    REDIS_TOKENS_SET_NAME,
)
from .crud import storage

from schemas.movie import Movie
from ..short_urls.redis import redis_tokens

log = logging.getLogger(__name__)


UNSAFE_METHODS = frozenset(
    {
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
    }
)

# Определяет параметры проверки подлинности с помощью статического API токена
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


def save_storage_state(
    request: Request,
    background_tasks: BackgroundTasks,
):
    yield
    if request.method in UNSAFE_METHODS:
        log.info("Add background task to save storage.")
        background_tasks.add_task(storage.save_state)


def validate_api_token(
    api_token: HTTPAuthorizationCredentials,
):
    # Проверяет наличие API токена в Redis хранилище
    if redis_tokens.sismember(REDIS_TOKENS_SET_NAME, api_token.credentials):
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
    # Require token only for unsafe methods; allow safe methods without token
    if request.method not in UNSAFE_METHODS:
        return

    validate_api_token(api_token=api_token)


def validate_basic_auth(
    credentials: HTTPBasicCredentials | None,
):
    # Проверяем, что предоставленные учетные данные являются действительными
    if (
        credentials
        and credentials.username in USERS_DB
        and USERS_DB[credentials.username] == credentials.password
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

    # Require auth only for unsafe methods; allow safe methods without auth
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
