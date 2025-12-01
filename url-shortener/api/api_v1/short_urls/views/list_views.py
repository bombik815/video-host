from fastapi import (
    APIRouter,
    status,
)


from schemas.short_url import ShortUrl, ShortUrlCreate
from api.api_v1.short_urls.crud import storage

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
