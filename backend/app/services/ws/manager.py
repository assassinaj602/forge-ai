"""
WebSocket Connection & Session Manager for Real-time Streaming
"""
from typing import Dict, List
from fastapi import WebSocket

class WebSocketManager:
    """Manages active WebSocket client connections."""
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, user_id: str, websocket: WebSocket):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)

    def disconnect(self, user_id: str, websocket: WebSocket):
        if user_id in self.active_connections:
            if websocket in self.active_connections[user_id]:
                self.active_connections[user_id].remove(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]

    async def send_json(self, websocket: WebSocket, data: dict):
        await websocket.send_json(data)

ws_manager = WebSocketManager()
