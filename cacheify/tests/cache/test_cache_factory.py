import pytest, os
from pytest import MonkeyPatch
from cacheify.cache.cache_factory import CacheFactory, SingletonCacheFactory
from cacheify.cache.local.local_cache import LocalCache
from cacheify.cache.redis.redis_cache import RedisCache

@pytest.fixture(autouse=True)
def reset_singleton():
    """Fixture to clear the singleton instance between tests."""
    SingletonCacheFactory._instances.clear()

def test_get_local_cache_with_custom_key():
    factory = CacheFactory(cache_type='local')
    config = {'key': 'custom_local_key'}
    cache = factory.get_cache(config=config)
    assert isinstance(cache, LocalCache)
    assert cache.key == 'custom_local_key'

def test_get_redis_cache_with_custom_key():
    factory = CacheFactory(cache_type='redis')
    config = {'key': 'custom_redis_key'}
    cache = factory.get_cache(config=config)
    assert isinstance(cache, RedisCache)
    assert cache.key == 'custom_redis_key'

def test_invalid_cache_type():
    factory = CacheFactory(cache_type='invalid')
    with pytest.raises(ValueError, match='Invalid cache type'):
        factory.get_cache()

def test_singleton_cache_factory_local_cache(monkeypatch: MonkeyPatch):
    """Test that SingletonCacheFactory creates a LocalCache by default."""
    # Ensure the environment variable is not set
    monkeypatch.delenv('CACHE_TYPE', raising=False)
    
    cache_factory = SingletonCacheFactory()
    cache = cache_factory.get_cache(config={'key': 'local_key'})
    
    assert isinstance(cache, LocalCache)
    assert cache.key == 'local_key'

def test_singleton_cache_factory_redis_cache_with_env(monkeypatch: MonkeyPatch):
    """Test that SingletonCacheFactory creates a RedisCache when CACHE_TYPE is set to 'redis'."""
    monkeypatch.setenv('CACHE_TYPE', 'redis')
    
    cache_factory = SingletonCacheFactory()
    cache = cache_factory.get_cache(config={'key': 'redis_key'})
    
    assert isinstance(cache, RedisCache)
    assert cache.key == 'redis_key'

def test_singleton_cache_factory_is_singleton():
    """Test that SingletonCacheFactory returns the same instance."""
    instance1 = SingletonCacheFactory()
    instance2 = SingletonCacheFactory()
    
    assert instance1 is instance2, "SingletonCacheFactory should return the same instance"

def test_singleton_cache_factory_with_invalid_cache_type(monkeypatch: MonkeyPatch):
    """Test that SingletonCacheFactory raises ValueError for an invalid cache type."""
    monkeypatch.setenv('CACHE_TYPE', 'invalid')
    
    with pytest.raises(ValueError, match="Invalid cache type"):
        SingletonCacheFactory().get_cache()

def test_cache_factory_respects_cache_type_change():
    """Test that CacheFactory respects changes in cache type."""
    cache_factory_local = CacheFactory(cache_type='local')
    cache_local = cache_factory_local.get_cache(config={'key': 'local_key'})
    assert isinstance(cache_local, LocalCache)
    
    cache_factory_redis = CacheFactory(cache_type='redis')
    cache_redis = cache_factory_redis.get_cache(config={'key': 'redis_key'})
    assert isinstance(cache_redis, RedisCache)

def test_singleton_factory_respects_cache_type_change(monkeypatch: MonkeyPatch):
    """Test that SingletonCacheFactory respects environment variable change across instances."""
    monkeypatch.setenv('CACHE_TYPE', 'local')
    instance1 = SingletonCacheFactory()
    cache1 = instance1.get_cache(config={'key': 'local_key'})
    assert isinstance(cache1, LocalCache)

    # This will not change the cache factory type as the singleton is already initialized
    monkeypatch.setenv('CACHE_TYPE', 'redis')
    instance2 = SingletonCacheFactory()
    cache2 = instance2.get_cache(config={'key': 'redis_key'})
    
    # Cache is still LocalCache due to singleton behavior
    assert isinstance(cache2, LocalCache)

def test_singleton_cache_factory_new_instance_with_new_env(monkeypatch: MonkeyPatch):
    """Test that after reinitializing the singleton with a new environment variable, the cache type changes."""
    monkeypatch.setenv('CACHE_TYPE', 'local')
    instance1 = SingletonCacheFactory()
    cache1 = instance1.get_cache(config={'key': 'local_key'})
    assert isinstance(cache1, LocalCache)

    # Reset the singleton to simulate a new instance
    SingletonCacheFactory._instances.clear()

    monkeypatch.setenv('CACHE_TYPE', 'redis')
    instance2 = SingletonCacheFactory()
    cache2 = instance2.get_cache(config={'key': 'redis_key'})
    
    assert isinstance(cache2, RedisCache)
