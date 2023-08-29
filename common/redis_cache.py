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
        return redis_client.set(keyword, data)

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
            # if redis_client.hexists(keyword):
            #     return redis_client.get(keyword)
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
