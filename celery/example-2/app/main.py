# app/main.py

from fastapi import FastAPI
from celery_worker import send_email_task
import time

app = FastAPI()


@app.get("/")
def root():
    return {"message": "FastAPI + Celery example running!"}


@app.get("/generate-report")
def generate_report(email: str):
    # Simulate report generation
    print("Generating report...")
    time.sleep(2)  # simulate CPU or IO processing

    # Offload email sending task to Celery
    send_email_task.delay(email)

    return {
        "status": "Report generated",
        "message": f"Email will be sent to {email} shortly"
    }

