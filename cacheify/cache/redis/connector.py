import redis
from utils import get_env_var
from cacheify.cache.singleton import Singleton

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
        # Initialize the connection pool and create Redis connection
        url_connection = get_env_var('REDIS_URL', 'redis://localhost:6379/0')
        decode_responses = get_env_var("REDIS_DECODE_RESPONSES", False, bool)
        self._pool = redis.ConnectionPool.from_url(
            url_connection,
            decode_responses=decode_responses
        )
        # Set up the connection attribute
        self._conn = redis.StrictRedis(connection_pool=self._pool)

    @property
    def conn(self) -> redis.StrictRedis:
        return self._conn