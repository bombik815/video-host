from typing import Annotated

from fastapi import Depends, APIRouter

from schemas.short_url import ShortUrl

from .dependencies import prefetch_short_urls
from .crud import SHORT_URLS


router = APIRouter(prefix="/short-urls", tags=["Short URLs"])


"""
Возвращает список всех сокращенных ссылок

Возвращает:
    list[ShortUrl]: список объектов сокращенных ссылок

"""


@router.get("/", response_model=list[ShortUrl])
def read_short_urls_list():
    return SHORT_URLS


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
