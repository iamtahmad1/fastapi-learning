import time
import logging
import sys
from fastapi import FastAPI, Request

# Configure logging
logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

app = FastAPI()

# Middleware for logging request details
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    logger.info(f"Incoming request: {request.method} {request.url}")
    
    response = await call_next(request)  # Process request
    
    process_time = time.time() - start_time
    logger.info(f"Completed request: {request.method} {request.url} in {process_time:.2f}s with status {response.status_code}")
    
    return response

@app.get("/")
async def home():
    n_list=[]
    for n in range(100000):
        n_list.append(n*n)
    print(n_list)
    return {"message": "Welcome to FastAPI!"}

@app.get("/error")
async def error():
    raise ValueError("Test error")  # Triggers ERROR log
