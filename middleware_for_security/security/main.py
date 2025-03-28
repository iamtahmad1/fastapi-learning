from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware

app=FastAPI()

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch( self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        return response
    
app.add_middleware(SecurityHeadersMiddleware)

@app.get("/")
async def root():
    return {"message": "Hello, Secure FastAPI!"}