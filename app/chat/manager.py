from typing import Dict

from fastapi import WebSocket

from app.users.models import Users


# class ConnectionManager:
#     def __init__(self):
#         self.active_connections: Dict[str, WebSocket] = {}
#
#     async def connect(self, websocket: WebSocket, user_id: str):
#         await websocket.accept()
#         self.active_connections[user_id] = websocket
#
#     def disconnect(self, user_id: str):
#         del self.active_connections[user_id]
#
#     async def send_personal_message(self, message: str, user_id: str):
#         websocket = self.active_connections.get(user_id)
#         if websocket:
#             await websocket.send_text(message)
#
#     async def broadcast(self, message: str):
#         for websocket in self.active_connections.values():
#             await websocket.send_text(message)

class ConnectionManager:
    def __init__(self):
        self.active_connections = {}

    async def connect(self, websocket: WebSocket, client_id: int):
        await websocket.accept()
        self.active_connections[client_id] = websocket

    def disconnect(self, user_id: int):
        del self.active_connections[user_id]

    async def send_personal_message(self, message: str, recipient_id: int, client_id: int):

        websocket = self.active_connections.get(recipient_id)
        if websocket:
            await websocket.send_text(message)

    async def broadcast(self, message: str):
        for websocket in self.active_connections.values():
            await websocket.send_text(message)


manager = ConnectionManager()
