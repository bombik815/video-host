from typing import Annotated

from annotated_types import Len, MaxLen
from pydantic import AnyHttpUrl, BaseModel

DescriptonString = Annotated[
    str,
    MaxLen(200),
]


class ShortUrlBase(BaseModel):
    target_url: AnyHttpUrl
    description: DescriptonString


class ShortUrlCreate(ShortUrlBase):
    """
    Модель создания сокращенной ссылки
    """

    slug: Annotated[
        str,
        Len(min_length=3, max_length=10),
    ]
    description: DescriptonString = ""


class ShortUrlUpdate(ShortUrlBase):
    """Модель для обновления информации о сокращенной ссылке"""


class ShortUrlPartialUpdate(BaseModel):
    target_url: AnyHttpUrl | None = None
    description: DescriptonString | None = None


class ShortUrlRead(ShortUrlBase):
    """Модель для чтения данный по короткой ссылке"""

    slug: str
    description: str


class ShortUrl(ShortUrlBase):
    """
    Модель сокращенной ссылки
    """

    slug: str
    visits: int = 42
