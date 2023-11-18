import asyncio
import json
from typing import Dict

from fastapi import WebSocket
from redis import asyncio as aioredis

from app.config import settings
from app.utils.dependencies import GetRedis


class ConnectionManager:
    def __init__(self, redis: aioredis.Redis):
        self.active_connections: Dict[int, WebSocket] = {}
        self.redis = redis

    async def connect(self, websocket: WebSocket, client_id: int):
        await websocket.accept()
        await self.redis.hset("active_connections", client_id, str(websocket))
        # self.active_connections[client_id] = websocket

    def disconnect(self, user_id: int):
        # del self.active_connections[user_id]
        self.redis.hdel("active_connections", user_id)

    async def send_personal_message(self, message: str, recipient_id: int, client_id: int):
        # websocket = self.active_connections.get(recipient_id)
        websocket = await self.redis.hget("active_connections", recipient_id)
        if websocket:
            # await websocket.send_text(message)
            await self.redis.publish(websocket, message)

    async def broadcast(self, message: str):
        # for websocket in self.active_connections.values():
        #     await websocket.send_text(message)
        active_connections = await self.redis.hvals("active_connections")
        for websocket in active_connections:
            # await websocket.send_text(message)
            await self.redis.publish(websocket, message)

# manager = ConnectionManager(redis=GetRedis)


class RedisPubSubManager:
    def __init__(self, host='localhost', port=6379):
        self.redis_host = host
        self.redis_port = port
        self.pubsub = None

    async def _get_redis_connection(self) -> aioredis.Redis:
        return aioredis.Redis(host=self.redis_host,
                              port=self.redis_port,
                              auto_close_connection_pool=False)

    async def connect(self) -> None:
        self.redis_connection = await self._get_redis_connection()
        self.pubsub = self.redis_connection.pubsub()

    async def _publish(self, room_id: str, message: str) -> None:
        await self.redis_connection.publish(room_id, message)

    async def subscribe(self, client_id, recipient_id) -> aioredis.Redis:
        await self.pubsub.subscribe(f'{(client_id, recipient_id)}')
        return self.pubsub

    async def unsubscribe(self, room_id: str) -> None:
        await self.pubsub.unsubscribe(room_id)


class WebSocketManager:
    def __init__(self):
        self.rooms: dict = {}
        self.active_connections: Dict[str, WebSocket] = {}
        self.pubsub_client = RedisPubSubManager(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

    async def add_user_to_room(self, client_id: int, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections[client_id] = websocket

        await self.pubsub_client.connect()
        pubsub_subscriber = await self.pubsub_client.subscribe(client_id)
        asyncio.create_task(self._pubsub_data_reader(pubsub_subscriber))

    async def create_private_room(self, client_id: int, recipient_id: int, websocket: WebSocket) -> None:
        print('--------CREATE---------')
        await websocket.accept()
        self.active_connections[f'{(client_id, recipient_id)}'] = websocket

        await self.pubsub_client.connect()
        print(self.pubsub_client.pubsub.channels)
        pubsub_subscriber = await self.pubsub_client.subscribe(client_id, recipient_id)
        asyncio.create_task(self._pubsub_data_reader(pubsub_subscriber))
        print(self.pubsub_client.pubsub.channels)
        print('==================================')

    async def broadcast_to_room(self, room_id: str, message: str) -> None:
        await self.pubsub_client._publish(room_id, message)

    async def delete_users_connection(self, client_id: int, recipient_id, websocket: WebSocket) -> None:
        print('--------DELETE---------')
        print(f'{(client_id, recipient_id)}')
        del self.active_connections[f'{(client_id, recipient_id)}']
        print(self.pubsub_client.pubsub.channels)
        await self.pubsub_client.unsubscribe(f'{(client_id, recipient_id)}')
        print(self.pubsub_client.pubsub.channels)

    async def _pubsub_data_reader(self, pubsub_subscriber):
        while True:
            message = await pubsub_subscriber.get_message(ignore_subscribe_messages=True)
            if message is not None:
                print(f"{message=}")
                data = json.loads(message['data'])
                socket_id = data.get('private_room')
                print(f"{socket_id=}")
                print(f"{self.active_connections=}")
                socket = self.active_connections.get(f"{tuple(socket_id[::-1])}")
                print(f"{socket=}")
                if socket:
                    message_data = f" User #{data.get('user_id')} wrote: {data.get('message')}"
                    await socket.send_text(message_data)
                print(f"User #{socket_id} WS = {socket}")
                print('============')


socket_manager = WebSocketManager()
