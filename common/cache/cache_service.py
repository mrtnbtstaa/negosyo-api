from typing import Any

from .base import BaseCache
from .django_cache import DjangoCache


class CacheService:

    _cache: BaseCache = DjangoCache()

    def __new__(cls):
        raise TypeError("CacheService cannot be instantiated.")

    @classmethod
    def store(
        cls,
        key: str,
        value: Any,
        ttl: int | None = None,
    ) -> None:
        cls._cache.store(
            key=key,
            value=value,
            ttl=ttl,
        )

    @classmethod
    def store_many(
        cls,
        data: dict[str, Any],
        ttl: int | None = None,
    ) -> list[str]:
        return cls._cache.store_many(
            data=data,
            ttl=ttl,
        )

    @classmethod
    def get(
        cls,
        key: str,
        default: Any = None,
    ) -> Any:
        return cls._cache.get(
            key=key,
            default=default,
        )

    @classmethod
    def get_many(
        cls,
        keys: list[str],
    ) -> dict[str, Any]:
        return cls._cache.get_many(
            keys=keys,
        )

    @classmethod
    def remove(
        cls,
        key: str,
    ) -> bool:
        return cls._cache.remove(
            key=key,
        )

    @classmethod
    def remove_many(
        cls,
        keys: list[str],
    ) -> None:
        cls._cache.remove_many(
            keys=keys,
        )

    @classmethod
    def exists(
        cls,
        key: str,
    ) -> bool:
        return cls._cache.exists(
            key=key,
        )

    @classmethod
    def increment(
        cls,
        key: str,
        delta: int = 1,
    ) -> int:
        return cls._cache.increment(
            key=key,
            delta=delta,
        )

    @classmethod
    def decrement(
        cls,
        key: str,
        delta: int = 1,
    ) -> int:
        return cls._cache.decrement(
            key=key,
            delta=delta,
        )

    @classmethod
    def touch(
        cls,
        key: str,
        ttl: int,
    ) -> bool:
        return cls._cache.touch(
            key=key,
            ttl=ttl,
        )

    @classmethod
    def clear(
        cls,
    ) -> None:
        cls._cache.clear()