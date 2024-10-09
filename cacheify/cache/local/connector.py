import redis
import fakeredis
from cache.singleton import Singleton

class RedisConnector(metaclass=Singleton):
    """
    RedisConnector is a singleton class that manages the connection to a Redis database.
    It initializes a connection pool and provides a Redis connection instance.
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