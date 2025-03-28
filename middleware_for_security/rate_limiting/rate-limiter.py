# Need redis to be running 
# docker run -d --name redis -p 6379:6379 redis


from fastapi import FastAPI, Request, Depends
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
import redis.asyncio as redis
from fastapi.responses import JSONResponse

app = FastAPI()

@app.on_event("startup")
async def startup():
    redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
    await FastAPILimiter.init(redis_client)

@app.get("/limited", dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def limited_api():
    return{"message": "This is limited to 10 requets per minutes"}


#Custom blocking message, 429 is too many request error code

@app.exception_handler(429)
async def custom_too_many_requests_handler(request: Request, exc):
    return JSONResponse(
        status_code=429,
        content={
            "error": "Too many requests",
            "message": "You have exceeded your rate limit. Try again in 60 seconds."
        },
    )


# Test: for i in {1..10}; do curl -i http://127.0.0.1:8000/limited; done
