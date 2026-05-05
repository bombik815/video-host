import secrets
from abc import ABC, abstractmethod


class AbstractTokensHelper(ABC):
    """
    Абстрактный базовый класс для работы с токенами.
    Определяет интерфейс для проверки, добавления и генерации токенов.
    Наследники должны реализовать методы token_exist, add_token,
    delete_token и get_tokens.

    Основные методы:
    - token_exist(token): проверяет наличие токена в хранилище
    - add_token(token): добавляет токен в хранилище
    - generate_token(): генерирует случайный токен (классовый метод)
    - generate_and_save_token(): генерирует и сохраняет токен
    """

    @abstractmethod
    def token_exist(self, token: str) -> bool:
        pass

    @abstractmethod
    def add_token(self, token: str) -> None:
        pass

    @abstractmethod
    def get_tokens(self) -> list[str]:
        pass

    @abstractmethod
    def delete_token(self, token: str) -> None:
        pass

    @classmethod
    def generate_token(cls) -> str:
        return secrets.token_urlsafe(16)

    def generate_and_save_token(self) -> str:
        token = self.generate_token()
        self.add_token(token)
        return token


AbstractTokenHelper = AbstractTokensHelper
