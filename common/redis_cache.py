import time
import redis.client
from redis import Redis
from config import redis_host, redis_port

from fastapi import HTTPException, status

from common.logger import logger
from common.utils import time_check


class RedisOperation:
    @staticmethod
    def redis_connection() -> redis.client.Redis:
        """
        This static method used to make redis connection with given host and port.
        :return: redis.client.Redis
        """
        redis_client = Redis(host=redis_host, port=redis_port, db=0)
        logger.info(f"Redis connection is Established.")
        return redis_client

    @staticmethod
    def set_cache_data(keyword: str, data) -> bool:
        """
        This static method used to set the data in redis.
        :param keyword: keyword which is used store data.
        :param data: Actual data which we are storing in redis.
        :return: bool
        """
        redis_client = RedisOperation.redis_connection()
        logger.info(f"Data has been saved into Redis.")
        # the data will expire in 1hr after setting up in redis cache
        return redis_client.setex(keyword, 3600, data)

    @staticmethod
    def get_cache_data(keyword: str) -> bytes:
        """
        This static method retrieves the data from cache.
        :param keyword: keyword which is used identify the respective data.
        :return: cache data in bytes
        """
        start_time = time.perf_counter()
        try:
            redis_client = RedisOperation.redis_connection()
            logger.info(f"fetching the Cache data.")
            return redis_client.get(keyword)

        except Exception as err:
            raise HTTPException(
                detail=f"Error in getting data from cache and Error - {str(err)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        finally:
            logger.info(
                f"Time taken to get data from cache {time_check(start_time, time.perf_counter())}"
            )


class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.redis = redis.StrictRedis(host=redis_host, port=redis_port, db=0)
        self.cache_key = "lru_cache"

    def get(self, key) -> bytes | None:
        """
        Get's the data from redis cache.
        :param key: cache key
        :return: bytes
        """
        # Check if the key exists in the cache
        if self.redis.hexists(self.cache_key, key):
            # Move the key to the front of the LRU list
            self.redis.zadd(self.cache_key + "_lru", {key: 0})
            return self.redis.hget(self.cache_key, key).decode("utf-8")
        else:
            return None

    def set(self, key: str, value: str) -> None:
        """
        Set's the data into redis cache.
        :param key: user provided which is used to store the data into redis cache.
        :param value: recommendation data from mongo.
        :return: None
        """
        # Check if the cache is at capacity
        if self.redis.hlen(self.cache_key) >= self.capacity:
            # Remove the least recently used item
            lru_key = self.redis.zrange(self.cache_key + "_lru", 0, 0)[0]
            self.redis.hdel(self.cache_key, lru_key)
            self.redis.zrem(self.cache_key + "_lru", lru_key)

        # Set the new key-value pair
        self.redis.hset(self.cache_key, key, value)

        # Add the key to the front of the LRU list
        self.redis.zadd(self.cache_key + "_lru", {key: 0})

    def delete(self, key):
        # Remove a key from the cache
        if self.redis.hexists(self.cache_key, key):
            self.redis.hdel(self.cache_key, key)
            self.redis.zrem(self.cache_key + "_lru", key)

    def clear(self):
        # Clear the entire cache
        self.redis.delete(self.cache_key)
        self.redis.delete(self.cache_key + "_lru")


cache = LRUCache(4)
