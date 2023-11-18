import asyncio
import json
from typing import Dict

from fastapi import WebSocket
from redis import asyncio as aioredis

from app.config import settings


class RedisPubSubManager:
    def __init__(self, host="localhost", port=6379):
        self.redis_host = host
        self.redis_port = port
        self.pubsub = None

    async def _get_redis_connection(self) -> aioredis.Redis:
        return aioredis.Redis(host=self.redis_host, port=self.redis_port, auto_close_connection_pool=False)

    async def connect(self) -> None:
        self.redis_connection = await self._get_redis_connection()
        self.pubsub = self.redis_connection.pubsub()

    async def _publish(self, room_id: str, message: str) -> None:
        await self.redis_connection.publish(room_id, message)

    async def subscribe(self, client_id, recipient_id) -> aioredis.Redis:
        await self.pubsub.subscribe(f"{(client_id, recipient_id)}")
        return self.pubsub

    async def unsubscribe(self, room_id: str) -> None:
        await self.pubsub.unsubscribe(room_id)


class WebSocketManager:
    def __init__(self):
        self.rooms: dict = {}
        self.active_connections: Dict[str, WebSocket] = {}
        self.pubsub_client = RedisPubSubManager(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

    async def create_private_room(self, client_id: int, recipient_id: int, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections[f"{(client_id, recipient_id)}"] = websocket

        await self.pubsub_client.connect()
        pubsub_subscriber = await self.pubsub_client.subscribe(client_id, recipient_id)
        asyncio.create_task(self._pubsub_data_reader(pubsub_subscriber))

    async def broadcast_to_room(self, room_id: str, message: str) -> None:
        await self.pubsub_client._publish(room_id, message)

    async def delete_users_connection(self, room_id: str, websocket: WebSocket) -> None:
        del self.active_connections[room_id]
        await self.pubsub_client.unsubscribe(room_id)

    async def _pubsub_data_reader(self, pubsub_subscriber):
        while True:
            message = await pubsub_subscriber.get_message(ignore_subscribe_messages=True)
            if message is not None:
                data = json.loads(message["data"])
                socket_id = data.get("private_room")
                socket = self.active_connections.get(f"{tuple(socket_id[::-1])}")
                if socket:
                    message_data = f" User #{data.get('user_id')} wrote: {data.get('message')}"
                    await socket.send_text(message_data)


socket_manager = WebSocketManager()
