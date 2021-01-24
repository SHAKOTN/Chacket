import os

from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from chacket.endpoints import router


def create_app() -> FastAPI:
    app = FastAPI()
    app.mount("/static", StaticFiles(directory=os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "chacket/static")), name="static")
    app.include_router(router)
    return app
