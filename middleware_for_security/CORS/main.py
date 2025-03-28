from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import HTMLResponse
import html

app = FastAPI()

# ✅ Custom Security Headers Middleware
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        return response

# ✅ Custom CORS Middleware
class CustomCORS(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["Access-Control-Allow-Origin"] = "https://trusteddomain.com"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST"
        response.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type"
        return response

# ✅ Register Middleware
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(CustomCORS)

# ✅ Secure Endpoint (Escaping User Input)
@app.get("/greet", response_class=HTMLResponse)
async def greet_user(name: str):
    safe_name = html.escape(name)  # ✅ Prevents XSS
    return f"<h1>Hello, {safe_name}!</h1>"

