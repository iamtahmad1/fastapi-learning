from fastapi import FastAPI, HTTPException
import logging

app = FastAPI()
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

@app.get("/log-test")
async def log_test():
    logging.info("This is an info log")
    logging.warning("This is a warning log")
    return {"message": "Check logs in the terminal"}