import asyncio
import time

async def async_api_call(n):
    print(f"Calling API {n}...")
    await asyncio.sleep(2)
    print(f"API {n} response received")

async def main():
    start_time = time.time()
    await asyncio.gather(async_api_call(1), async_api_call(2), async_api_call(3))
    print(f"Total time (async): {time.time() - start_time:.2f} seconds")

asyncio.run(main())
