from unittest import TestCase

from api.api_v1.auth.services import redis_tokens
from testing import ensure_testing_environment

"""Проверяет наличие переменной окружения TESTING=1.
 Raises:
     OSError: Если переменная окружения TESTING не установлена в значение '1'.
 """
ensure_testing_environment()


class RedisTokensHelperTestCase(TestCase):

    def test_generate_and_save_token(self) -> None:
        """Проверяет, что сгенерированный токен сохраняется и существует в системе."""

        new_token = redis_tokens.generate_and_save_token()
        expected_exist = True
        self.assertTrue(
            expected_exist,
            redis_tokens.token_exist(new_token),
        )

    def test_generated_token_is_not_empty(self) -> None:
        """Проверяет, что сгенерированный токен не является пустой строкой."""
        new_token = redis_tokens.generate_and_save_token()
        self.assertTrue(
            len(new_token) > 0,
            "Токен не должен быть пустым",
        )

    def test_generated_tokens_are_unique(self) -> None:
        """Проверяет, что каждый вызов генерирует уникальный токен."""
        token_one = redis_tokens.generate_and_save_token()
        token_two = redis_tokens.generate_and_save_token()
        self.assertNotEqual(
            token_one,
            token_two,
            "Каждый сгенерированный токен должен быть уникальным",
        )

    def test_non_existent_token_does_not_exist(self) -> None:
        # Проверяет, что произвольный токен,
        # не сохранённый в системе, не существует.
        fake_token = f"missing-token-{__name__}"
        self.assertFalse(
            redis_tokens.token_exist(fake_token),
            "Несуществующий токен не должен быть найден в системе",
        )
