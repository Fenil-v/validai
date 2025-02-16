import redis
import asyncio

async def get_redis():
    redis = await asyncio.to_thread(redis.asyncio.Redis, host='localhost', port=6379, db=0)
    return redis