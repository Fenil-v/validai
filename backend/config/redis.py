
# type: ignore
import aioredis 

REDIS_URL = "redis://localhost:6379"

async def get_redis():
    # Create a Redis client using aioredis 2.x
    redis = await aioredis.from_url(REDIS_URL, decode_responses=True)
    return redis
