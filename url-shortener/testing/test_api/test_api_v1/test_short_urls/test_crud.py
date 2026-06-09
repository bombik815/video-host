from unittest import TestCase

from api.api_v1.short_urls.crud import storage
from schemas.short_url import (
    ShortUrl,
    ShortUrlCreate,
    ShortUrlPartialUpdate,
    ShortUrlUpdate,
)
from testing import ensure_testing_environment

ensure_testing_environment()


class ShortUrlStorageUpdateTestCase(TestCase):
    def setUp(self) -> None:
        """Создаёт тестовую короткую ссылку перед каждым тестом."""
        self.short_url = self.create_short_url()

    def tearDown(self) -> None:
        """Удаляет тестовую короткую ссылку после каждого теста."""
        storage.delete(self.short_url)

    def create_short_url(self) -> ShortUrl:
        """Создаёт и возвращает короткую ссылку для тестов."""
        short_url_in = ShortUrlCreate(
            slug="foo",
            description="a foo description",
            target_url="https://example.com",
        )
        return storage.create(short_url_in)

    def test_update(self) -> None:
        """Проверяет полное обновление короткой ссылки."""
        short_url_update = ShortUrlUpdate(**self.short_url.model_dump())
        old_description = self.short_url.description
        short_url_update.description *= 2

        updated_short_url = storage.update(
            short_url=self.short_url,
            short_url_in=short_url_update,
        )
        self.assertNotEqual(
            old_description,
            updated_short_url.description,
        )
        self.assertEqual(
            short_url_update,
            ShortUrlUpdate(**updated_short_url.model_dump()),
        )

    def test_update_partial(self) -> None:
        """Проверяет частичное обновление короткой ссылки."""
        short_url_partial_update = ShortUrlPartialUpdate(
            description=self.short_url.description * 2,
        )
        old_description = self.short_url.description
        updated_short_url = storage.update_partial(
            short_url=self.short_url,
            short_url_in=short_url_partial_update,
        )
        self.assertNotEqual(
            old_description,
            updated_short_url.description,
        )
        self.assertEqual(
            short_url_partial_update.description,
            updated_short_url.description,
        )
