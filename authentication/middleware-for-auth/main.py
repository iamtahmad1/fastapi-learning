from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from jose import jwt, JWTError
from typing import Optional
from datetime import datetime, timedelta
from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str


# Constants
SECURITY_KEY = "mysecretkey"  # Replace with your actual secret key
ALGORITHM = "HS256"

app = FastAPI()

fake_users_db={
    "admin_user": {"username":"admin_user", "role":"admin"},
    "normal_user": {"username": "normal_user", "role":"user"}
}

def create_access_token(data: dict, expires_delta: Optional[timedelta]= None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    return jwt.encode(to_encode, SECURITY_KEY, algorithm=ALGORITHM)

# RBAC Middleware
class RBACMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Define which roles can access which paths
        role_permissions = {
            "/users": "admin",  # Only admins can view users
            "/tasks/delete": "admin",  # Only admins can delete tasks
        }

        token = request.headers.get("Authorization")
        if token and token.startswith("Bearer "):
            token = token.split(" ")[1]
            try:
                # Decode the JWT token
                payload = jwt.decode(token, SECURITY_KEY, algorithms=[ALGORITHM])
                user_role = payload.get("role", "user")  # Default to "user"

                # Check role-based access control
                for path, required_role in role_permissions.items():
                    if request.url.path.startswith(path) and user_role != required_role:
                        return JSONResponse(status_code=403, content={"detail": "Forbidden: Insufficient permissions"})
            except JWTError:
                return JSONResponse(status_code=401, content={"detail": "Invalid token"})

        return await call_next(request)

# Add middleware to FastAPI app
app.add_middleware(RBACMiddleware)
tasks = {1: "Task 1", 2: "Task 2"}

@app.post("/token")
def login(request: LoginRequest):
    user = fake_users_db.get(request.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid username")
    token = create_access_token({"sub": request.username, "role": user["role"]})
    return {"access_token": token, "token_type": "bearer"}

# Sample API Endpoints
@app.get("/users")
async def get_users():
    return {"message": "List of users (admin only)"}

@app.delete("/tasks/delete/{task_id}")
async def delete_task(task_id: int):
    return {"message": f"Task {task_id} deleted (admin only)"}

@app.get("/public")
async def public_endpoint():
    return {"message": "This is a public endpoint, accessible by anyone"}
