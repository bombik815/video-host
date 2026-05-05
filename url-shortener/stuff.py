from redis import Redis

from core import config

redis = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB,
    decode_responses=True,
)


def main() -> None:
    print(redis.ping())
    redis.set("name", "Alex")
    redis.set("foo", "bar")
    redis.set("number", "44")
    print("name:", redis.get("name"))
    print(
        [
            redis.get("foo"),
            redis.get("number"),
            redis.get("spam"),
        ],
    )


if __name__ == "__main__":
    main()
