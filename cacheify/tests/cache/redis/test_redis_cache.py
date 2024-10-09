import pytest
import threading, time
from collections.abc import Iterable
from cacheify.cache.redis.redis_cache import RedisCache

@pytest.fixture
def cache() -> RedisCache:
    return RedisCache()

def test_set_and_get(cache: RedisCache):
    cache.set('key1', 'value1')
    assert cache.get('key1') == 'value1'

def test_set_with_ttl(cache: RedisCache):
    cache.set('key_ttl', 'value_ttl', ttl=1)
    # Immediately check if the key is accessible
    assert cache.get('key_ttl') == 'value_ttl'
    # Wait for more than the TTL duration (e.g., 1.5 seconds)
    time.sleep(1.5)
    # After the TTL has expired, the key should no longer exist
    assert cache.get('key_ttl') is None

def test_get_non_existent_key(cache: RedisCache):
    assert cache.get('non_existent_key') is None

def test_set_and_get_collection(cache: RedisCache):
    test_list = [1, 2, 3]
    cache.set('key2', test_list)
    result = cache.get('key2')
    assert result == test_list
    assert result is not test_list  # Ensure deep copy

def test_pop(cache: RedisCache):
    cache.set('key3', 'value3')
    assert cache.pop('key3') == 'value3'
    assert cache.get('key3') is None

def test_pop_collection(cache: RedisCache):
    test_dict = {'a': 1}
    cache.set('key4', test_dict)
    result = cache.pop('key4')
    assert result == test_dict
    assert result is not test_dict  # Ensure deep copy

def test_keys(cache: RedisCache):
    cache.set('key5', 'value5')
    cache.set('key6', 'value6')
    keys = cache.keys()
    assert 'key5' in keys
    assert 'key6' in keys

@pytest.mark.filterwarnings("ignore::pottery.exceptions.InefficientAccessWarning")
def test_values(cache: RedisCache):
    cache.set('key7', 'value7')
    cache.set('key8', 'value8')
    values = cache.values()
    assert 'value7' in values
    assert 'value8' in values

def test_expire_method(cache: RedisCache):
    cache.set('key_expire', 'value_expire')
    # Verify that the key is accessible right after setting it
    assert cache.get('key_expire') == 'value_expire'
    cache.expire(1)
    # Check that the key is still accessible right after setting the expiration
    assert cache.get('key_expire') == 'value_expire'
    # Wait for more than the TTL (1.5 seconds)
    time.sleep(1.5)
    # After the TTL has expired, the key should no longer exist
    assert cache.get('key_expire') is None

def test_clear(cache: RedisCache):
    cache.set('key9', 'value9')
    cache.clear()
    assert cache.get('key9') is None
    assert isinstance(cache.keys(), Iterable)
    assert len(cache.keys()) == 0

def test_set_overwrite(cache: RedisCache):
    cache.set('key10', 'value10')
    cache.set('key10', 'new_value10')
    assert cache.get('key10') == 'new_value10'

def test_set_none_value(cache: RedisCache):
    cache.set('key11', None)
    assert cache.get('key11') is None

def test_items(cache: RedisCache):
    cache.clear()
    cache.set('key12', 'value12')
    cache.set('key13', 'value13')
    items = cache.items()
    assert ('key12', 'value12') in items
    assert ('key13', 'value13') in items
    assert len(items) == 2

def test_items_empty_cache(cache: RedisCache):
    cache.clear()
    items = cache.items()
    assert len(items) == 0

@pytest.mark.filterwarnings("ignore::pottery.exceptions.InefficientAccessWarning")
def test_iter(cache: RedisCache):
    cache.set('key14', 'value14')
    cache.set('key15', 'value15')
    keys = [key for key in cache]
    assert 'key14' in keys
    assert 'key15' in keys

def test_cache_len(cache: RedisCache):
    cache.clear()
    cache.set('key16', 'value16')
    cache.set('key17', 'value17')
    assert len(cache) == 2

def test_thread_safety(cache: RedisCache):
    
    def set_values():
        for i in range(100):
            cache.set(f'key{i}', f'value{i}')

    threads = [threading.Thread(target=set_values) for _ in range(10)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    for i in range(100):
        assert cache.get(f'key{i}') == f'value{i}'