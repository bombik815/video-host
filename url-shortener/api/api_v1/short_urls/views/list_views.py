from fastapi import (
    APIRouter,
    status,
    Depends,
)

from api.api_v1.short_urls.dependencies import (
    api_token_or_user_basic_auth_required_for_unsafe_methods,
)
from schemas.short_url import (
    ShortUrl,
    ShortUrlCreate,
    ShortUrlRead,
)
from api.api_v1.short_urls.crud import storage

router = APIRouter(
    prefix="/short-urls",
    tags=["Short URLs"],
    dependencies=[
        Depends(api_token_or_user_basic_auth_required_for_unsafe_methods),
    ],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Unauthenticated. Only for unsafe method.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid API token",
                    },
                },
            },
        },
    },
)


"""
Возвращает список всех сокращенных ссылок:
    list[ShortUrl]: список объектов сокращенных ссылок

"""


@router.get("/", response_model=list[ShortUrlRead])
def read_short_urls_list() -> list[ShortUrl]:
    return storage.get()


"""
Создает новую сокращенную ссылку

Параметры:
    short_url_create (ShortUrlCreate): данные для создания сокращенной ссылки

Возвращает:
    ShortUrl: созданный объект сокращенной ссылки
"""


@router.post("/", response_model=ShortUrlRead, status_code=status.HTTP_201_CREATED)
def create_short_url(
    short_url_create: ShortUrlCreate,
):
    return storage.create(short_url_create)
