import redis.asyncio as redis
from app.core.config import settings

class RedisClient:
    def __init__(self):
        self.redis_url = settings.REDIS_URL
        self.client = None

    async def connect(self):
        self.client = await redis.from_url(self.redis_url, encoding="utf-8", decode_responses=True)

    async def close(self):
        if self.client:
            await self.client.close()

    async def get_client(self) -> redis.Redis:
        if not self.client:
            await self.connect()
        return self.client

redis_client = RedisClient()

async def get_redis() -> redis.Redis:
    return await redis_client.get_client()
