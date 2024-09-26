from typing import List
import redis.asyncio as redis


class RedisManager:
    def __init__(self, redis_host: str = "localhost", redis_port: int = 6379):
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.redis = None

    async def connect(self):
        if not self.redis:
            # Establish an asynchronous connection using redis-py
            self.redis = redis.Redis(host=self.redis_host, port=self.redis_port)

    async def store_message(self, user_id: int, message: str):
        """Store a message in Redis for a specific user."""
        await self.connect()
        # Use the lpush command to add a message to the list
        await self.redis.lpush(f"message_queue:{user_id}", message)

    async def get_queued_messages(self, user_id: int) -> List[str]:
        """Retrieve and remove all messages from the Redis queue for a specific user."""
        await self.connect()
        messages = []
        # Loop to pop all messages from the list until it's empty
        while True:
            message = await self.redis.rpop(f"message_queue:{user_id}")
            if not message:
                break
            messages.append(message.decode())  # Decode the message from bytes to string
        return messages
