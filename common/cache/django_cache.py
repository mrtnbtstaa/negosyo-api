from typing import Any

from django.core.cache import cache

from .base import BaseCache


class DjangoCache(BaseCache):
    """
    Django cache implementation.

    Uses Django's cache framework, allowing the
    backend to be configured through settings.py.
    """

    def store(
        self,
        key: str,
        value: Any,
        ttl: int | None = None,
    ) -> None:
        cache.set(
            key=key,
            value=value,
            timeout=ttl,
        )

    def store_many(
        self,
        data: dict[str, Any],
        ttl: int | None = None,
    ) -> list[str]:
        return cache.set_many(
            data=data,
            timeout=ttl,
        )

    def get(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        return cache.get(
            key=key,
            default=default,
        )

    def get_many(
        self,
        keys: list[str],
    ) -> dict[str, Any]:
        return cache.get_many(
            keys=keys,
        )

    def remove(
        self,
        key: str,
    ) -> bool:
        return cache.delete(
            key=key,
        )

    def remove_many(
        self,
        keys: list[str],
    ) -> None:
        cache.delete_many(
            keys=keys,
        )

    def exists(
        self,
        key: str,
    ) -> bool:
        return cache.has_key(
            key=key,
        )

    def increment(
        self,
        key: str,
        delta: int = 1,
    ) -> int:
        return cache.incr(
            key=key,
            delta=delta,
        )

    def decrement(
        self,
        key: str,
        delta: int = 1,
    ) -> int:
        return cache.decr(
            key=key,
            delta=delta,
        )

    def touch(
        self,
        key: str,
        ttl: int,
    ) -> bool:
        return cache.touch(
            key=key,
            timeout=ttl,
        )

    def clear(self) -> None:
        cache.clear()