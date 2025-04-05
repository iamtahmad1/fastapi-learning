from fastapi import FastAPI
import time

app = FastAPI()

@app.get("/sync")
def sync_endpoint():
    time.sleep(5)  # Simulating a slow operation
    return {"message": "This was a synchronous response"}
