import threading
from typing import Optional
from redis import Redis
from pottery import RedisDict
from cache.cacheable import Cacheable
from .connector import RedisConnector

class LocalCache(Cacheable):
    def __init__(self, *, key: str='cache', redis_client: Optional[Redis]=None, **kwargs):
        self._key = key
        self._cache = RedisDict(redis=self._normalize_masters(redis_client), key=key)
        self._semaphore = threading.Semaphore(1)  # A binary semaphore to allow one thread at a time

    def _normalize_masters(self, redis_client: Optional[Redis]=None) -> Redis:
        return redis_client if isinstance(redis_client, Redis) else RedisConnector()
    
    @property
    def key(self):
        return self._key

    def get(self, key):
        self._semaphore.acquire()  # Acquire semaphore to ensure thread safety
        try:
            return self._cache.get(key)
        finally:
            self._semaphore.release()  # Release semaphore so that other threads can proceed

    def set(self, key, value, ttl=None):
        self._semaphore.acquire()
        try:
            self._cache[key] = value
            self._cache.redis.expire(self._cache.key, ttl) if ttl else None
        finally:
            self._semaphore.release()

    def pop(self, key):
        self._semaphore.acquire()
        try:
            return self._cache.pop(key)
        finally:
            self._semaphore.release()

    def keys(self):
        """
        This is an O(n) operation, so performance may degrade with larger caches.
        Avoid using this method in performance-critical code.
        """
        self._semaphore.acquire()
        try:
            return self._cache.keys()
        finally:
            self._semaphore.release()

    def values(self):
        self._semaphore.acquire()
        try:
            return self._cache.values()
        finally:
            self._semaphore.release()

    def items(self):
        self._semaphore.acquire()
        try:
            return self._cache.items()
        finally:
            self._semaphore.release()

    def expire(self, ttl, key=None, **kwargs):
        self._semaphore.acquire()
        try:
            return self._cache.redis.expire(key or self._cache.key, ttl)
        finally:
            self._semaphore.release()

    def clear(self):
        self._semaphore.acquire()
        try:
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
            return iter(self._cache)
        finally:
            self._semaphore.release()

    def __len__(self):
        self._semaphore.acquire()
        try:
            return len(self._cache)
        finally:
            self._semaphore.release()