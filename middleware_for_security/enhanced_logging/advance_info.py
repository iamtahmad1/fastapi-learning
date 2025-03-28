import time
import json
import logging
import requests
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

# ✅ Configure Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = FastAPI()

# ✅ Function to get geolocation data
def get_geolocation(ip: str):
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json", timeout=2)
        geo_data = response.json()
        return {
            "city": geo_data.get("city", "Unknown"),
            "region": geo_data.get("region", "Unknown"),
            "country": geo_data.get("country", "Unknown"),
            "org": geo_data.get("org", "Unknown"),
            "timezone": geo_data.get("timezone", "Unknown"),
        }
    except Exception:
        return {"error": "Unable to fetch geolocation"}

# ✅ Middleware for Advanced Logging
class AdvancedLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # 🔹 Extract Request Data
        client_ip = request.client.host
        client_port = request.client.port
        method = request.method
        url = request.url.path
        user_agent = request.headers.get("user-agent", "Unknown")
        referer = request.headers.get("referer", "None")
        origin = request.headers.get("origin", "None")

        # 🔹 Get GeoLocation
        geo_info = get_geolocation(client_ip)

        # 🔹 Log Request Body (Only for JSON payloads)
        try:
            body = await request.body()
            request_body = json.loads(body.decode()) if body else {}
        except json.JSONDecodeError:
            request_body = {}

        # 🔹 Filter Headers (Exclude sensitive ones)
        filtered_headers = {k: v for k, v in request.headers.items() if k.lower() not in ["authorization", "cookie"]}

        logging.info(f"""
        📥 Request:
        ────────────
        🔹 IP: {client_ip}:{client_port}
        🔹 User-Agent: {user_agent}
        🔹 Geo: {geo_info}
        🔹 Referer: {referer}
        🔹 Origin: {origin}
        🔹 Method: {method} {url}
        🔹 Headers: {filtered_headers}
        🔹 Body: {request_body}
        """)

        # 🔹 Process Request
        response = await call_next(request)

        # 🔹 Log Response Data
        process_time = time.time() - start_time
        response_body = b""
        async for chunk in response.body_iterator:
            response_body += chunk

        response_body_str = response_body.decode() if response_body else "No Content"

        logging.info(f"""
        📤 Response:
        ────────────
        🔹 Status: {response.status_code}
        🔹 Processing Time: {process_time:.3f}s
        🔹 Body: {response_body_str}
        """)

        return Response(content=response_body, status_code=response.status_code, headers=dict(response.headers), media_type=response.media_type)

# ✅ Register Middleware
app.add_middleware(AdvancedLoggingMiddleware)

# ✅ Example API Endpoint
@app.post("/data")
async def process_data(data: dict):
    return {"message": "Data received", "data": data}
