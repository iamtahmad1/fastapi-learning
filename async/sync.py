import time

def sync_api_call(n):
    print(f"Calling API {n}...")
    time.sleep(2)  # Simulating API call delay
    print(f"API {n} response received")

start_time = time.time()

sync_api_call(1)
sync_api_call(2)
sync_api_call(3)

print(f"Total time (sync): {time.time() - start_time:.2f} seconds")
