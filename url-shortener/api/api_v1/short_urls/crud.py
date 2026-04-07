import logging

from pydantic import BaseModel, ValidationError
from redis import Redis

from core import config
from core.config import SHORT_URLS_STORAGE_FILEPATH
from schemas.short_url import (
    ShortUrl,
    ShortUrlCreate,
    ShortUrlUpdate,
    ShortUrlPartialUpdate,
)

log = logging.getLogger(__name__)

redis = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB_SHORT_URLS,
    decode_responses=True,
)


class ShortUrlStorage(BaseModel):

    def save_short_url(self, short_url: ShortUrl) -> None:
        redis.hset(
            name=config.REDIS_SHORT_URLS_HASH_NAME,
            key=short_url.slug,
            value=short_url.model_dump_json(),
        )

    """
    Возвращает список всех сохраненных объектов ShortUrl.
    
    Возвращает:
        list[ShortUrl]: список всех сохраненных объектов ShortUrl
    """

    def get(self) -> list[ShortUrl]:
        # Получение список значение ShortUrl from Redis через hvals
        return [
            ShortUrl.model_validate_json(value)
            for value in redis.hvals(name=config.REDIS_SHORT_URLS_HASH_NAME)
        ]

    """
    Возвращает объект ShortUrl по его slug.

    Параметры:
        slug (str): slug объекта ShortUrl

    Возвращает:
        ShortUrl | None: объект ShortUrl если найден, иначе None
    """

    def get_by_slug(self, slug: str) -> ShortUrl | None:
        # Получаем запись с REDIS по slug
        if data := redis.hget(
            name=config.REDIS_SHORT_URLS_HASH_NAME,
            key=slug,
        ):
            return ShortUrl.model_validate_json(data)

    """
    Создает объект ShortUrl на основе переданных параметров.

    Параметры:
        short_url_create (ShortUrlCreate): объект ShortUrlCreate, содержащий параметры для создания ShortUrl

    Возвращает:
        ShortUrl: созданный объект ShortUrl
    """

    def create(self, short_url_create: ShortUrlCreate) -> ShortUrl:
        short_url = ShortUrl(**short_url_create.model_dump())
        # Этот код сохраняет информацию о короткой ссылке в Redis
        self.save_short_url(short_url)
        log.info("Created new short url %s.", short_url)
        return short_url

    def update(
        self,
        short_url: ShortUrl,
        short_url_in: ShortUrlUpdate,
    ):

        for field_name, value in short_url_in:
            setattr(short_url, field_name, value)
        self.save_short_url(short_url)  # save to REDIS
        return short_url

    def update_partial(
        self,
        short_url: ShortUrl,
        short_url_in: ShortUrlPartialUpdate,
    ):

        # Применяем частичное обновление только для полей, которые были явно переданы в запросе.
        # model_dump(exclude_unset=True) — фича Pydantic v2: возвращает словарь ТОЛЬКО с теми полями,
        # которые были заданы (не пропущены) в модели ShortUrlPartialUpdate.
        # Это предотвращает перезапись отсутствующих полей значениями по умолчанию/None.
        for field_name, value in short_url_in.model_dump(exclude_unset=True).items():
            setattr(short_url, field_name, value)
        self.save_short_url(short_url)  # save to REDIS
        return short_url

    def delete_by_slug(self, slug: str) -> None:
        # Удаляем запись с REDIS
        redis.hdel(
            config.REDIS_SHORT_URLS_HASH_NAME,
            slug,
        )

    def delete(self, short_url: ShortUrl) -> None:
        self.delete_by_slug(slug=short_url.slug)


storage = ShortUrlStorage()
