from fastapi import FastAPI
import time
import asyncio


app = FastAPI()

@app.get("/sync")
def sync_endpoint():
    for i in range(5):
        time.sleep(1)
        print(i)
    time.sleep(5)  # Simulating a slow operation
    return {"message": "This was a synchronous response"}


@app.get("/async")
async def async_endpoint():
    await asyncio.sleep(5)
    for i in range(5):
        time.sleep(1)
        print(i)  # Non-blocking
    return {"message": "This was an asynchronous response"}

