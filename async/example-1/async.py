from fastapi import FastAPI
import asyncio

app = FastAPI()

@app.get("/async")
async def async_endpoint():
    await asyncio.sleep(5)  # Non-blocking
    return {"message": "This was an asynchronous response"}
