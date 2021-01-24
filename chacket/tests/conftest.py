import pytest

from chacket.app import create_app


@pytest.fixture
def chacket_app():
    chacket = create_app()
    yield chacket
