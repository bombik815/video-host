from abc import ABC, abstractmethod


class AbstractUsersHelper(ABC):
    """
    Абстрактный базовый класс для работы с пользователями.
    Определяет интерфейс для получения пароля и валидации пользователей.
    Наследники должны реализовать метод get_user_password.

    Основные методы:
    - get_user_password(username): получает пароль пользователя из хранилища
    - check_passwords_natch(password1, password2): сравнивает два пароля
    - validate_user_password(username, password):
      проверяет корректность пароля пользователя
    """

    @abstractmethod
    def get_user_password(self, username: str) -> str | None:
        """Передаем:
        - имя пользователя
        - return: пароль по пользователю, если найден
        """

    @classmethod
    def check_passwords_natch(cls, password1: str, password2: str) -> bool:
        """
        Проверка паролей на совпадение
        - return: True если есть, иначе False
        """
        return password1 == password2

    def validate_user_password(self, username: str, password: str) -> bool:
        """
        Передаем:
        - username - чей пароль проверить
        - password - переданный пароль, сверить с паролем в БД
        - return: True если есть, иначе False
        """

        db_password = self.get_user_password(username)
        if db_password is None:
            return False
        return self.check_passwords_natch(password1=db_password, password2=password)
