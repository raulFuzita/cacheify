import threading
from typing import Union, List
from redis import Redis
from pottery import Redlock, RedisDict
from cacheify.cache.cacheable import Cacheable
from .connector import RedisConnector

class RedisCache(Cacheable):
    def __init__(self, *, key: str='cache', masters: Union[Redis, list, None]=None, auto_release_time: float=10, **kwargs):
        self._key = key
        self.masters = self._normalize_masters(masters)
        self.auto_release_time = auto_release_time
        self._cache = RedisDict(redis=self.masters[0], key=key)
        self._semaphore = threading.Semaphore(1)  # A binary semaphore to allow one thread at a time

    def _normalize_masters(self, masters: Union[Redis, list, None]=None) -> List[Redis]:
        if isinstance(masters, list):
            return masters
        elif isinstance(masters, Redis):
            return [masters]
        else:
            return [RedisConnector()]

    @property
    def redlock(self) -> Redlock:
        """A property to get a new Redlock instance."""
        return Redlock(key=self._key, masters=self.masters, auto_release_time=self.auto_release_time)
    
    @property
    def key(self):
        return self._key

    def get(self, key):
        self._semaphore.acquire()  # Acquire semaphore to ensure thread safety
        try:
            with self.redlock:
                return self._cache.get(key)
        finally:
            self._semaphore.release()  # Release semaphore so that other threads can proceed

    def set(self, key, value, ttl=None):
        self._semaphore.acquire()
        try:
            with self.redlock:
                self._cache[key] = value
                self._cache.redis.expire(self._cache.key, ttl) if ttl else None
        finally:
            self._semaphore.release()

    def pop(self, key):
        self._semaphore.acquire()
        try:
            with self.redlock:
                return self._cache.pop(key)
        finally:
            self._semaphore.release()

    def _balance_release_time(self, cache_size: int) -> int:
        # extra_time =  size * base_time_per_item + overhead_time
        extra_time = (cache_size * 0.001) + 0.5
        return self.auto_release_time + extra_time

    def keys(self):
        """
        This is an O(n) operation, so performance may degrade with larger caches.
        The Redlock's `auto_release_time` is adjusted based on cache size to balance performance and consistency.
        Avoid using this method in performance-critical code.
        """
        self._semaphore.acquire()
        try:
            redlock = self.redlock
            redlock.auto_release_time = self._balance_release_time(len(self._cache))
            with redlock:
                return self._cache.keys()
        finally:
            self._semaphore.release()

    def values(self):
        self._semaphore.acquire()
        try:
            with self.redlock:
                return self._cache.values()
        finally:
            self._semaphore.release()

    def items(self):
        self._semaphore.acquire()
        try:
            with self.redlock:
                return self._cache.items()
        finally:
            self._semaphore.release()

    def expire(self, ttl, key=None, **kwargs):
        self._semaphore.acquire()
        try:
            with self.redlock:
                return self._cache.redis.expire(key or self._cache.key, ttl)
        finally:
            self._semaphore.release()

    def clear(self):
        self._semaphore.acquire()
        try:
            with self.redlock:
                self._cache.clear()
        finally:
            self._semaphore.release()

    def __iter__(self):
        """
        Returns an iterator over the cache. 
        This performs an O(n) Redis operation, which can be slow and is 
        not recommended if performance is critical.
        """
        self._semaphore.acquire()
        try:
            redlock = self.redlock
            redlock.auto_release_time = self._balance_release_time(len(self._cache))
            with redlock:
                return iter(self._cache)
        finally:
            self._semaphore.release()

    def __len__(self):
        self._semaphore.acquire()
        try:
            with self.redlock:
                return len(self._cache)
        finally:
            self._semaphore.release()
