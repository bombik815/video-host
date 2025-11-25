from typing import Annotated

from fastapi import (
    Depends,
    APIRouter,
    status,
)


from schemas.short_url import ShortUrl, ShortUrlCreate

from .dependencies import prefetch_short_urls
from .crud import storage

router = APIRouter(prefix="/short-urls", tags=["Short URLs"])


"""
Возвращает список всех сокращенных ссылок

Возвращает:
    list[ShortUrl]: список объектов сокращенных ссылок

"""


@router.get("/", response_model=list[ShortUrl])
def read_short_urls_list() -> list[ShortUrl]:
    return storage.get()


"""
Создает новую сокращенную ссылку

Параметры:
    short_url_create (ShortUrlCreate): данные для создания сокращенной ссылки

Возвращает:
    ShortUrl: созданный объект сокращенной ссылки
"""


@router.post("/", response_model=ShortUrl, status_code=status.HTTP_201_CREATED)
def create_short_url(
    short_url_create: ShortUrlCreate,
):
    return storage.create(short_url_create)


"""
Возвращает объект сокращенной ссылки по ее slug

Параметры:
    slug (str): slug сокращенной ссылки

Возвращает:
    ShortUrl: объект сокращенной ссылки

Исключения:
    HTTPException: 404 если сокращенная ссылка не найдена
"""


@router.get("/{slug}/", response_model=ShortUrl)
def read_short_url_details(
    url: Annotated[ShortUrl, Depends(prefetch_short_urls)],
) -> ShortUrl:
    return url
