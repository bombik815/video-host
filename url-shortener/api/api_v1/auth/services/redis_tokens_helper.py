from redis import Redis

from api.api_v1.auth.services.tokens_helper import AbstractTokensHelper
from core import config


class RedisTokensHelper(AbstractTokensHelper):
    """
    Реализация работы с токенами через Redis.
    Хранит токены в Redis в виде множества (SET).

    Основные методы:
    - token_exist(token): проверяет наличие токена в Redis SET через SISMEMBER
    - add_token(token): добавляет токен в Redis через SADD
    - get_tokens(): возвращает список всех токенов из Redis SET
    """

    def __init__(self, host: str, port: int, db: int, tokens_set_name: str) -> None:
        self.redis = Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=True,
        )
        self.tokens_set = tokens_set_name

    def token_exist(self, token: str) -> bool:
        return bool(self.redis.sismember(self.tokens_set, token))

    def add_token(self, token: str) -> None:
        self.redis.sadd(self.tokens_set, token)

    def get_tokens(self) -> list[str]:
        return list(self.redis.smembers(self.tokens_set))


RedisTokenHelper = RedisTokensHelper


redis_tokens = RedisTokensHelper(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB_TOKENS,
    tokens_set_name=config.REDIS_TOKENS_SET_NAME,
)
