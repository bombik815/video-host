import secrets
from abc import ABC, abstractmethod


class AbstractTokenHelper(ABC):
    """
    проверка наличия токена;
    добавление токена в хранилище;
    генерация нового токена;
    """

    @abstractmethod
    def token_exist(self, token: str) -> bool:
        pass

    @abstractmethod
    def add_token(self, token: str) -> None:
        pass

    @classmethod
    def generate_token(cls) -> str:
        return secrets.token_urlsafe(16)

    def generate_and_save_token(self) -> str:
        token = self.generate_token()
        self.add_token(token)
        return token
