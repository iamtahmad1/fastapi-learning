import time
import json
import logging
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

logging.basicConfig(level=logging.INFO, format="%(asctime)s -%(levelname)s -%(message)s")

app=FastAPI()


class AdvancedLogging(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        client_ip = request.client.host
        method = request.method
        url = request.url.path
        headers = dict(request.headers)

        try: 
            body = await request.body()
            request_body = json.loads(body.decode()) if body else{}
        except json.JSONDecodeError:
            request_body= {}

        logging.info(f"📥 Request: {client_ip} {method} {url} | Headers: {headers} | Body: {request_body}")

        response = await call_next(Request)
             
        process_time = time.time() - start_time
        response_body = b""
        async for chunk in response.body_iterator:
            response_body += chunk

        response_body_str = response_body.decode() if response_body else "No Content"

        logging.info(f"📤 Response: {method} {url} | Status: {response.status_code} | Time: {process_time:.3f}s | Body: {response_body_str}")

        return Response(content=response_body, status_code=response.status_code, headers=dict(response.headers), media_type=response.media_type)
    

app.add_middleware(AdvancedLogging)

@app.post("/data")
async def process_data(data: dict):
    return {"message": "Data received", "data": data}