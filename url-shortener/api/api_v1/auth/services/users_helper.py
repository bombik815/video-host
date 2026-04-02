from abc import ABC, abstractmethod


class AbstractUsersHelper(ABC):
    """
    - Получение пароля по username;
    - Совпадает ли пароль с переданным пользователю;
    """

    @abstractmethod
    def get_user_password(self, username: str) -> str | None:
        """Передаем:
        - имя пользователя
        - return: пароль по пользователю, если найден
        """
        pass

    @classmethod
    def check_passwords_natch(cls, password1: str, password2: str) -> bool:
        """
        Проверка паролей на совпадение
        - retur: True если есть, иначе False
        """
        return password1 == password2

    def validate_user_password(self, username: str, password: str) -> bool:
        """
        Передаем:
        - username - чей пароль проверить
        - password - переданный пароль, сверить с паролем в БД
        - retur: True если есть, иначе False
        """

        db_password = self.get_user_password(username)
        if db_password is None:
            return False
        return self.check_passwords_natch(password1=db_password, password2=password)
