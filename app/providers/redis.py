import redis.asyncio as Redis


class RedisConnection:
    __REDIS_CONNECTION__ = None

    @staticmethod
    async def create_connection() -> Redis:
        if RedisConnection.__REDIS_CONNECTION__ is None:
            RedisConnection.__REDIS_CONNECTION__ = await Redis.from_url(
                "redis://redis:6379/0"
            )
        return RedisConnection.__REDIS_CONNECTION__

    @staticmethod
    async def close_connection() -> Redis:
        if RedisConnection.__REDIS_CONNECTION__:
            await RedisConnection.__REDIS_CONNECTION__.close()
