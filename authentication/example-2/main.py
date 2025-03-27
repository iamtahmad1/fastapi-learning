from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str


SECURITY_KEY = "SECRET_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

fake_users_db={
    "admin_user": {"username":"admin_user", "role":"admin"},
    "normal_user": {"username": "normal_user", "role":"user"}
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: Optional[timedelta]= None):
    print(data)
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    print(expire)

    print(to_encode.update({"exp": expire}))
    return jwt.encode(to_encode, SECURITY_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECURITY_KEY)
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None or role is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return {"username": username, "role": role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    
def admin_required(user: dict = Depends(get_current_user)):
    """Check if the user is an admin."""
    if user["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admins only")
    return user

app = FastAPI()

tasks = {1: "Task 1", 2: "Task 2"}

@app.post("/token")
def login(request: LoginRequest):
    user = fake_users_db.get(request.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid username")
    token = create_access_token({"sub": request.username, "role": user["role"]})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/users", dependencies=[Depends(admin_required)])
def get_users():
    """Only admins can access the users list."""
    return {"users": list(fake_users_db.keys())}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, user: dict = Depends(admin_required)):
    """Only admins can delete tasks."""
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    del tasks[task_id]
    return {"message": f"Task {task_id} deleted"}
