import logging

from pydantic import BaseModel, ValidationError

from core.config import SHORT_URLS_STORAGE_FILEPATH
from schemas.short_url import (
    ShortUrl,
    ShortUrlCreate,
    ShortUrlUpdate,
    ShortUrlPartialUpdate,
)


log = logging.getLogger(__name__)

class ShortUrlStorage(BaseModel):
    slug_to_short_url: dict[str, ShortUrl] = {}

    def save_state(self) -> None:
        SHORT_URLS_STORAGE_FILEPATH.write_text(self.model_dump_json(indent=2))
        log.info("Saved short url to storage file.")

    @classmethod
    def from_state(cls) -> "ShortUrlStorage":
        if not SHORT_URLS_STORAGE_FILEPATH.exists():
            log.info("Short url storage file does not exist.")
            return ShortUrlStorage()
        return cls.model_validate_json(SHORT_URLS_STORAGE_FILEPATH.read_text())


    """
    Возвращает список всех сохраненных объектов ShortUrl.
    
    Возвращает:
        list[ShortUrl]: список всех сохраненных объектов ShortUrl
    """

    def get(self) -> list[ShortUrl]:
        return list(self.slug_to_short_url.values())

    """
    Возвращает объект ShortUrl по его slug.

    Параметры:
        slug (str): slug объекта ShortUrl

    Возвращает:
        ShortUrl | None: объект ShortUrl если найден, иначе None
    """

    def get_by_slug(self, slug: str) -> ShortUrl | None:
        return self.slug_to_short_url.get(slug)

    """
    Создает объект ShortUrl на основе переданных параметров.

    Параметры:
        short_url_create (ShortUrlCreate): объект ShortUrlCreate, содержащий параметры для создания ShortUrl

    Возвращает:
        ShortUrl: созданный объект ShortUrl
    """

    def create(self, short_url_create: ShortUrlCreate) -> ShortUrl:
        short_url = ShortUrl(
            **short_url_create.model_dump(),
        )
        self.slug_to_short_url[short_url.slug] = short_url
        self.save_state() # save to json file
        return short_url

    def update(
        self,
        short_url: ShortUrl,
        short_url_in: ShortUrlUpdate,
    ):

        for field_name, value in short_url_in:
            setattr(short_url, field_name, value)
        self.save_state()  # save to json file
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
        self.save_state()  # save to json file
        return short_url

    def delete_by_slug(self, slug: str) -> None:
        self.slug_to_short_url.pop(slug, None)
        self.save_state()  # save to json file

    def delete(self, short_url: ShortUrl) -> None:
        self.delete_by_slug(slug=short_url.slug)

try:
    storage = ShortUrlStorage().from_state()
    log.warning("Recovered data from storage file.")
except ValidationError:
    storage = ShortUrlStorage()
    storage.save_state()
    log.warning("Rewritten storage file due to validation error.")
