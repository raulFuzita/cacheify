from cacheify.cache.cacheable import Cacheable
from cacheify.cache.local.local_cache import LocalCache
from cacheify.cache.redis.redis_cache import RedisCache

class CacheifyFactory:
    def __init__(self, cache_type: str='local'):
        self.cache_type = cache_type

    def get_cache(self, config: dict={}, **kwargs) -> Cacheable:
        if self.cache_type == 'local':
            return LocalCache(**config)
        elif self.cache_type == 'redis':
            return RedisCache(**config)
        raise ValueError('Invalid cache type')