import redis
import fakeredis
from cacheify.cache.singleton import Singleton

class RedisConnector(metaclass=Singleton):
    """
    RedisConnector is a singleton that uses fakeredis to simulate a Redis instance
    for local development and testing. It provides a shared, in-memory Redis-like
    connection without using a connection pool.
    """

    def __new__(cls, *args, **kwargs):
        # Check if an instance already exists
        if not hasattr(cls, '_instance'):
            # Create a new instance and initialize connection pool
            cls._instance = super(RedisConnector, cls).__new__(cls, *args, **kwargs)
            cls._instance._initialize_connection()

        # Return the Redis connection instead of the instance
        return cls._instance._conn
    
    def _initialize_connection(self) -> None:
        # Use fakeredis for local development/testing
        self._server = fakeredis.FakeServer()  # Shared server for singleton behavior
        self._conn = fakeredis.FakeStrictRedis(server=self._server)

    @property
    def conn(self) -> redis.StrictRedis:
        return self._conn