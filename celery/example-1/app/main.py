# app/main.py
from fastapi import FastAPI, status
from pydantic import BaseModel
from .celery_worker import send_email_task

app = FastAPI()

class UserSignup(BaseModel):
    email: str

@app.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(user: UserSignup):
    # Save user to DB (simulated)
    print(f"Registered user: {user.email}")

    # Queue welcome email
    send_email_task.delay(user.email)

    return {"message": "User registered successfully"}
