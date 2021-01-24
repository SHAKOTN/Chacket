import contextvars
import logging
import os
from logging.config import dictConfig

import aioredis
from aioredis import Redis
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from chacket.endpoints import router
from chacket.log_config import log_config

logger = logging.getLogger('logger')


context_redis: contextvars.ContextVar[Redis] = contextvars.ContextVar('redis')


def create_app() -> FastAPI:
    dictConfig(log_config)
    app = FastAPI()
    app.mount("/static", StaticFiles(directory=os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "chacket/static")), name="static")
    app.include_router(router)

    redis_host = os.getenv("REDIS_HOST", "redis")
    redis_port = os.getenv("REDIS_PORT", 6379)

    @app.on_event("startup")
    async def handle_startup():
        try:
            pool = await aioredis.create_redis_pool(
                (redis_host, redis_port), encoding='utf-8', maxsize=20
            )
            context_redis.set(pool)
            logger.info(f"Connected to Redis on {redis_host}:{redis_port}")
        except ConnectionRefusedError:
            logger.info(f"Cannot connect to Redis on {redis_host}:{redis_port}")
            return

    @app.on_event("shutdown")
    async def handle_shutdown():
        context_redis.get().close()
        logger.info(f"Closed Redis connection on {redis_host}:{redis_port}")

    return app
