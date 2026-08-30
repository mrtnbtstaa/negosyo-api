from abc import ABC, abstractmethod
from typing import Any


class BaseCache(ABC):
    """
    Base cache contract.

    Every cache implementation (Redis, Memcached,
    Database Cache, LocMemCache, etc.) should
    implement this interface.
    """

    @abstractmethod
    def store(
        self,
        key: str,
        value: Any,
        ttl: int | None = None,
    ) -> None:
        """Store a single cache entry."""
        ...

    @abstractmethod
    def store_many(
        self,
        data: dict[str, Any],
        ttl: int | None = None,
    ) -> list[str]:
        """Store multiple cache entries."""
        ...

    @abstractmethod
    def get(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        """Retrieve a cache entry."""
        ...

    @abstractmethod
    def get_many(
        self,
        keys: list[str],
    ) -> dict[str, Any]:
        """Retrieve multiple cache entries."""
        ...

    @abstractmethod
    def remove(
        self,
        key: str,
    ) -> bool:
        """Delete a cache entry."""
        ...

    @abstractmethod
    def remove_many(
        self,
        keys: list[str],
    ) -> None:
        """Delete multiple cache entries."""
        ...

    @abstractmethod
    def exists(
        self,
        key: str,
    ) -> bool:
        """Check whether a cache key exists."""
        ...

    @abstractmethod
    def increment(
        self,
        key: str,
        delta: int = 1,
    ) -> int:
        """Increment a numeric cache value."""
        ...

    @abstractmethod
    def decrement(
        self,
        key: str,
        delta: int = 1,
    ) -> int:
        """Decrement a numeric cache value."""
        ...

    @abstractmethod
    def touch(
        self,
        key: str,
        ttl: int,
    ) -> bool:
        """Update the expiration of an existing cache entry."""
        ...

    @abstractmethod
    def clear(self) -> None:
        """Remove every cache entry."""
        ...