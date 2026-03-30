
from redis import Redis


from core import config

# Этот код создаёт подключение к базе данных Redis. 
# Он использует конфигурацию из файла `core.config` для подключения к Redis, 
# указывая хост, порт и номер базы данных. 
# Созданный объект `redis_tokens` будет использоваться для взаимодействия с Redis, 
# при этом все ответы от сервера будут автоматически декодироваться в строки.
redis_tokens = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB_TOKENS,
    decode_responses=True,
)
