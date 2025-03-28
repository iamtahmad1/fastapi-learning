from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, Response
import html  # ✅ Used to escape HTML special characters

app = FastAPI()

# 🔹 Middleware to sanitize input and add security headers
@app.middleware("http")
async def security_middleware(request: Request, call_next):
    response = await call_next(request)

    # ✅ Add security headers
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    
    return response

@app.get("/greet", response_class=HTMLResponse)
async def greet_user(name: str):
    safe_name = html.escape(name)  # ✅ Escape user input to prevent XSS
    return f"<h1>Hello, {name}!</h1>"  # ✅ Now safe from XSS attacks
