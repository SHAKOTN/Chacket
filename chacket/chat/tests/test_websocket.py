from starlette.testclient import TestClient

from chacket.chat.main import app


def test_websocket_chat_init():
    client = TestClient(app)
    with client.websocket_connect("/ws/123") as websocket:
        # Get initial message with info about users in chat
        data = websocket.receive_text()
        assert "There are 0 active users in chat at the moment" == data
        # Send message and receive it back
        websocket.send_text("Hello!")
        hello = websocket.receive_text()
        assert "Hello!" == hello
        broadcast_message = websocket.receive_text()
        assert "Client #123 says: Hello!" == broadcast_message
