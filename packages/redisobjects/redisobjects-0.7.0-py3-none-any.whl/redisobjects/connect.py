from .redis_manager import RedisManager

from aioredis import create_connection

async def connect(address, **kwargs):
    connection = await create_connection(address, **kwargs)
    redis_manager = RedisManager(connection)
    return redis_manager
