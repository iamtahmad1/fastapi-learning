from fastapi import FastAPI, Request
import time
import logging

logging.basicConfig(level=logging.INFO)

app=FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time=time.time()
    response=await call_next(request)
    duration=time.time() - start_time
    logging.info(f"{request.method} {request.url.path} - {duration:.3f}s")
    return response

@app.get("/")
async def root():
    return {"message": "Hello, FastAPI!"}
