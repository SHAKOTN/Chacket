from starlette.testclient import TestClient


def test_get_basic_endpoint(chacket_app):
    with TestClient(chacket_app) as client:
        response = client.get("/")
        assert 200 == response.status_code
        assert response.is_redirect is False
