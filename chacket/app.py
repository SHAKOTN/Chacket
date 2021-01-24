import logging
import os
from logging.config import dictConfig

from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from chacket.endpoints import router
from chacket.log_config import log_config
from chacket.redis import chacket_redis

logger = logging.getLogger('logger')


def create_app() -> FastAPI:
    dictConfig(log_config)
    app = FastAPI()
    app.mount("/static", StaticFiles(directory=os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "chacket/static")), name="static")
    app.include_router(router)

    @app.on_event("startup")
    async def handle_startup():
        await chacket_redis.connect()

    @app.on_event("shutdown")
    async def handle_shutdown():
        await chacket_redis.disconnect()

    return app
