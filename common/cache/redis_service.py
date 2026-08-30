from redis import Redis
from django.core.cache import cache
from django.conf import settings
import json

redis_client = Redis.from_url(settings.REDIS_URL)

class RedisService:
    """
    Redis-specific operations.

    These methods are not part of Django's generic cache
    framework and are only available when using Redis.
    """

    def __new__(cls):
        raise TypeError("RedisService cannot be instantiated.")

    @classmethod
    def exists(cls, key: str) -> bool:
        return bool(
            redis_client.exists(key)
        )

    @classmethod
    def set_if_not_exists(
        cls,
        key: str,
        value: dict,
        ttl: int
    ) -> bool:
        return bool(
            redis_client.set(
                name=key,
                value=json.dumps(value),
                nx=True, # When set to true the value cannot be overwrite it will just return false if the key has already been set.
                ex=ttl
            )
        )

    @classmethod
    def set(
        cls,
        key: str,
        value: dict,
        ttl: int
    ) -> None:

        redis_client.set(
            name=key,
            value=json.dumps(value),
            ex=ttl
        )

    @classmethod
    def get(
        cls,
        key: str
    ) -> dict | None:

        value = redis_client.get(key)

        if value is None:
            return None

        return json.loads(value)

    @classmethod
    def delete(
        cls,
        key: str
    ) -> None:

        redis_client.delete(key)

    @classmethod
    def ping(cls) -> bool:
        return redis_client.ping()

    @classmethod
    def ttl(
        cls,
        key: str,
    ) -> int:
        """
        Returns:
            > 0 : seconds remaining
            -1  : key exists but has no expiration
            -2  : key does not exist
        """ 
        _key = cache.make_key(key)      
        return redis_client.ttl(_key)

    @classmethod
    def expire(
        cls,
        key: str,
        ttl: int,
    ) -> bool:
        return redis_client.expire(
            key,
            ttl,
        )

    @classmethod
    def persist(
        cls,
        key: str,
    ) -> bool:
        return redis_client.persist(key)

    @classmethod
    def keys(
        cls,
        pattern: str = "*",
    ) -> list[str]:
        return [
            key.decode()
            for key in redis_client.keys(pattern)
        ]

    @classmethod
    def scan(
        cls,
        cursor: int = 0,
        pattern: str = "*",
        count: int = 100,
    ) -> tuple[int, list[str]]:

        next_cursor, keys = redis_client.scan(
            cursor=cursor,
            match=pattern,
            count=count,
        )

        return (
            next_cursor,
            [key.decode() for key in keys]
        )

    @classmethod
    def db_size(cls) -> int:
        return redis_client.dbsize()

    @classmethod
    def flush_db(cls) -> None:
        redis_client.flushdb()

    @classmethod
    def flush_all(cls) -> None:
        redis_client.flushall()

    @classmethod
    def publish(
        cls,
        channel: str,
        message: str,
    ) -> int:
        return redis_client.publish(
            channel,
            message,
        )

    @classmethod
    def pipeline(cls):
        return redis_client.pipeline()

    @classmethod
    def lock(
        cls,
        name: str,
        timeout: int | None = None,
    ):
        return redis_client.lock(
            name=name,
            timeout=timeout,
        )