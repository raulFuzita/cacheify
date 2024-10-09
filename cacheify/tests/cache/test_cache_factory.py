import pytest
from cacheify.cache.cache_factory import CacheifyFactory
from cacheify.cache.local.local_cache import LocalCache
from cacheify.cache.redis.redis_cache import RedisCache

def test_get_local_cache_with_custom_key():
    factory = CacheifyFactory(cache_type='local')
    config = {'key': 'custom_local_key'}
    cache = factory.get_cache(config=config)
    assert isinstance(cache, LocalCache)
    assert cache.key == 'custom_local_key'

def test_get_redis_cache_with_custom_key():
    factory = CacheifyFactory(cache_type='redis')
    config = {'key': 'custom_redis_key'}
    cache = factory.get_cache(config=config)
    assert isinstance(cache, RedisCache)
    assert cache.key == 'custom_redis_key'

def test_invalid_cache_type():
    factory = CacheifyFactory(cache_type='invalid')
    with pytest.raises(ValueError, match='Invalid cache type'):
        factory.get_cache()