import pytest

from app import create_app


@pytest.fixture
def chacket_app():
    chacket = create_app()
    yield chacket
