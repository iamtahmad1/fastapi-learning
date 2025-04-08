# app/celery_worker.py
from celery import Celery
from time import sleep

celery_app = Celery(
    "worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1"
)

@celery_app.task
def send_email_task(email: str):
    sleep(3)  # simulate email latency
    print(f"[Celery]  Email sent to: {email}")
