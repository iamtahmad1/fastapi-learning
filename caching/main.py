from fastapi import FastAPI, Request
import aioredis
import json
import time
from loguru import logger

app = FastAPI()

# Connect to Redis
async def get_redis():
    return await aioredis.from_url("redis://localhost", decode_responses=True)

@app.middleware("http")
async def log_request_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(f"Request: {request.url.path} | Time Taken: {duration:.4f}s")
    return response

@app.get("/user/{user_id}")
async def get_user(user_id: int):
    redis = await get_redis()
    cache_key = f"user:{user_id}"

    # Check if data exists in Redis
    cached_data = await redis.get(cache_key)
    if cached_data:
        logger.info(f"Cache HIT for user {user_id}")
        return json.loads(cached_data)

    # Simulated database query (adding delay)
    logger.info(f"Cache MISS for user {user_id} - Fetching from DB")
    time.sleep(1)  # Simulating DB latency
    user_data = {"id": user_id, "name": f"User {user_id}", "age": 20 + user_id}

    # Store in Redis with TTL (300s)
    await redis.setex(cache_key, 300, json.dumps(user_data))

    return user_data
