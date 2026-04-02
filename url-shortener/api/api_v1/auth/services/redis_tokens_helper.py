from redis import Redis

from api.api_v1.auth.services.tokens_helper import AbstractTokenHelper
from core import config


class RedisTokenHelper(AbstractTokenHelper):
    """
    Реализация работы с токенами через Redis.
    Хранит токены в Redis в виде множества (SET).
    
    Основные методы:
    - token_exist(token): проверяет наличие токена в Redis SET через SISMEMBER
    - add_token(token): добавляет токен в Redis через SET
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
        self.redis.set(self.tokens_set, token)


redis_tokens = RedisTokenHelper(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB_TOKENS,
    tokens_set_name=config.REDIS_TOKENS_SET_NAME,
)
