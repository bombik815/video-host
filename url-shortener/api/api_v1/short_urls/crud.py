from pydantic import BaseModel

from schemas.short_url import ShortUrl, ShortUrlCreate


class ShortUrlStorage(BaseModel):
    slug_to_short_url: dict[str, ShortUrl] = {}

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
        ShortUrl | None: объект ShortUrl если найд��н, иначе None
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
        return short_url


storage = ShortUrlStorage()


storage.create(
    ShortUrlCreate(
        target_url="https://example.com",
        slug="example",
    )
)
storage.create(
    ShortUrlCreate(
        target_url="https://google.com",
        slug="search",
    ),
)
