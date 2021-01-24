import logging
import os
from typing import Optional

import aioredis
from aioredis import Redis

logger = logging.getLogger('logger')


class ChacketRedis:

    REDIS_HOST = os.getenv("REDIS_HOST", "redis")
    REDIS_PORT = os.getenv("REDIS_PORT", 6379)

    def __init__(self):
        self._redis = None

    @property
    def redis(self) -> Optional[Redis]:
        return self._redis

    @redis.setter
    def redis(self, redis: Redis) -> None:
        self._redis = redis

    async def connect(self):
        try:
            self.redis = await aioredis.create_redis_pool(
                (self.REDIS_HOST, self.REDIS_PORT), encoding='utf-8', maxsize=20
            )
            logger.info(f"Connected to Redis on {self.REDIS_HOST}:{self.REDIS_PORT}")
        except ConnectionRefusedError:
            logger.info(f"Cannot connect to Redis on {self.REDIS_HOST}:{self.REDIS_PORT}")
            return

    async def disconnect(self):
        if self.redis:
            self.redis.close()
            await self.redis.wait_closed()
            logger.info(f"Closed Redis connection on {self.REDIS_HOST}:{self.REDIS_PORT}")

        self.redis = None


chacket_redis = ChacketRedis()
