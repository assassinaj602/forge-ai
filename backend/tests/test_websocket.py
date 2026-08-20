import pytest
from fastapi.testclient import TestClient
from app.main import app

def test_websocket_chat_stream():
    client = TestClient(app)
    with client.websocket_connect("/api/v1/ws/chat?token=test_token") as websocket:
        websocket.send_json({"message": "Hello WebSocket", "provider": "mock", "model": "mock-v1"})
        
        start_msg = websocket.receive_json()
        assert start_msg["type"] == "start"
        
        chunk_msg = websocket.receive_json()
        assert chunk_msg["type"] == "chunk"
        assert "delta" in chunk_msg
