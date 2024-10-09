from abc import ABC, abstractmethod
from typing import Iterable, Optional, Any
from .json_types import JSONType

class Cacheable(ABC):
    
    @property
    @abstractmethod
    def key(self) -> Any:
        """
        An abstract property for getting the cache key. Each subclass must implement this property.
        """
        pass

    @abstractmethod
    def get(self, key: str) -> Any:
        pass

    @abstractmethod
    def set(self, key: str, value: JSONType, ttl: Optional[int]=None):
        """
        Set a JSON serializable value in the cache with an optional time-to-live (TTL).

        Args:
            key (str): The key under which the value is stored.
            value (JSONType): The value to be stored in the cache. Must be JSON serializable.
            ttl (Optional[int], optional): The time-to-live for the cache entry in seconds.
                                        If None, the entry does not expire. Defaults to None.
        """
        pass

    @abstractmethod
    def pop(self, key: str) -> Any:
        pass

    @abstractmethod
    def keys(self) -> Iterable:
        pass

    @abstractmethod
    def values(self) -> Iterable:
        pass

    @abstractmethod
    def items(self) -> Iterable:
        """Returns key-value pairs."""
        pass

    @abstractmethod
    def expire(self, ttl: int, key: Optional[str]=None, **kwargs) -> bool:
        """
        Expires a cache entry after a specified time-to-live (TTL).
        
        Args:
            ttl (int): The time-to-live in seconds after which the cache entry should expire.
            key (Optional[str], optional): The key of the cache entry to expire. If None, the method will use the key associated with the cacheable instance. Defaults to None.
                Note: Setting a key manually should only be done if necessary and with an understanding of the cache implementation.
            **kwargs: Additional keyword arguments that support the expiration logic in specific implementations of Cacheable.
                Each concrete implementation should document the supported keyword arguments in its own docstring if any.
        Returns:
            bool: True if the cache entry was successfully expired, False otherwise.
        """
        pass

    @abstractmethod
    def clear(self):
        """
        Clears the cache by removing all cached items.
        """
        pass

    @abstractmethod
    def __iter__(self) -> Iterable:
        """Iterates over cache keys."""
        pass

    @abstractmethod
    def __len__(self) -> int:
        pass