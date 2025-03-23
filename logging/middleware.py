from fastapi import FastAPI, Request
import logging

# Configure Logging
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s"
)

app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logging.info(f"Incoming request: {request.method} {request.url}")

    try:
        response = await call_next(request)
        if response.status_code >= 400 and response.status_code < 500:
            logging.warning(f"Warning: Client error {response.status_code} for {request.url}")  # WARNING Level
        return response
    except Exception as e:
        logging.error(f"Error processing request: {request.method} {request.url} - {str(e)}", exc_info=True)  # ERROR Level
        raise e

# Normal route (INFO)
@app.get("/")
async def home():
    return {"message": "Hello, FastAPI!"}

# Warning route (Client error)
@app.get("/warn")
async def warn():
    return {"message": "This is a warning example"}, 404  # Returns 404 (Warning)

# Error route (Server error)
@app.get("/error")
async def error():
    raise ValueError("This is a test error")  # Triggers ERROR log