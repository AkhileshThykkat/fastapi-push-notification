from fastapi import WebSocket
from typing import List, Dict
import asyncio

from schema import PushNotificationInput
from redis_queue import RedisManager


#  Connection Manager Class to handle WebSocket connections
class ConnectionManager:
    def __init__(self, redis_manager: RedisManager) -> None:
        self.active_connections: List[Dict[int, WebSocket]] = []
        self.redis_manager = (
            redis_manager  # Use RedisManager for handling message queues
        )

    async def connect(self, websocket: WebSocket, connection_id: int):
        await websocket.accept()
        self.active_connections.append({connection_id: websocket})
        await self._check_and_send_queued_messages(connection_id)

    def disconnect(self, user_id):
        for conn_dict in self.active_connections:
            if conn_dict.get(user_id):
                self.active_connections.remove(conn_dict)

    def get_ws(self, user_id: int) -> WebSocket:
        for conn_dict in self.active_connections:
            if conn_dict.get(user_id):
                return conn_dict[user_id]
        return None

    async def personal_message(self, message: PushNotificationInput):
        user_ws = self.get_ws(message.user_id)
        if user_ws:
            await user_ws.send_json(message.message)
            return True
        else:
            await self.redis_manager.store_message(message.user_id, message.message)
            return False

    async def _check_and_send_queued_messages(self, user_id: int):
        # When a user connects, check if they have queued messages in Redis
        user_ws = self.get_ws(user_id)
        if user_ws:
            # Get all queued messages from Redis and send them to the user
            messages = await self.redis_manager.get_queued_messages(user_id)
            for message in messages:
                await user_ws.send_json(message)

    async def ping(self, websocket: WebSocket):
        await websocket.send_text("ping")

    async def reply(self, websocket: WebSocket):
        await websocket.send_text("pong")

    async def pong(self, websocket: WebSocket):
        await self.reply(websocket)
        try:
            pong = await asyncio.wait_for(websocket.receive_text(), timeout=5)
            if pong == "pong":
                return True
            else:
                return False
        except asyncio.exceptions.TimeoutError as e:
            return False

    async def personal_notification(self, message: PushNotificationInput):
        # For personal notifications
        connection_check = self.get_ws(message.user_id)
        if connection_check:
            await connection_check.send_json(message.message)
            await asyncio.sleep(2)
            return True
        else:
            await self.redis_manager.store_message(message.user_id, message.message)
            return False


redis_manager = RedisManager()
wsok_manager = ConnectionManager(redis_manager)
