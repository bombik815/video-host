from pydantic import BaseModel, HttpUrl


class ShortUrlBase(BaseModel):
    target_url: str
    slug: str


class ShortUrl(ShortUrlBase):
    """
    Модель сокращенной ссылки
    """
