import asyncio
import aioredis
import json

async def populate_redis():
    redis = await aioredis.from_url("redis://localhost", decode_responses=True)

    users = {
        1: {"id": 1, "name": "Alice", "age": 25},
        2: {"id": 2, "name": "Bob", "age": 30},
        3: {"id": 3, "name": "Charlie", "age": 28}
    }

    for user_id, data in users.items():
        await redis.setex(f"user:{user_id}", 300, json.dumps(data))
        print(f"Stored: {user_id} -> {data}")

    await redis.close()

asyncio.run(populate_redis())
