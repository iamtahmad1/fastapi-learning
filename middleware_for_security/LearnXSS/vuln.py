from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/greet", response_class=HTMLResponse)
async def greet_user(name: str):
    return f"<h1>Hello, {name}!</h1>"  # ❌ XSS Vulnerability (User input is not sanitized)
