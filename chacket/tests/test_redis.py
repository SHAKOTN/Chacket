import os

import pytest
from chacket.redis import chacket_redis


@pytest.mark.asyncio
async def test_redis_pool_is_present():
    await chacket_redis.connect()
    assert chacket_redis.redis is not None
    assert (os.getenv("REDIS_HOST", "redis"), os.getenv("REDIS_PORT", 6379)) == chacket_redis.redis.address
    assert chacket_redis.redis.closed is False
