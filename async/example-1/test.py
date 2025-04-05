import requests
import time
import asyncio
import aiohttp

URL_SYNC = "http://127.0.0.1:8000/sync"
URL_ASYNC = "http://127.0.0.1:8000/async"

# Test Synchronous
def test_sync():
    start = time.time()
    responses = [requests.get(URL_SYNC) for _ in range(3)]
    end = time.time()
    print(f"Sync took: {end - start:.2f} seconds")

# Test Asynchronous
async def test_async():
    start = time.time()
    async with aiohttp.ClientSession() as session:
        tasks = [session.get(URL_ASYNC) for _ in range(3)]
        responses = await asyncio.gather(*tasks)
    end = time.time()
    print(f"Async took: {end - start:.2f} seconds")

print("Testing sync...")
test_sync()

print("Testing async...")
asyncio.run(test_async())
