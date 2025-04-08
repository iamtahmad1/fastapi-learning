# app/tasks.py
from datetime import datetime
from celery import shared_task

@shared_task
def cleanup_unverified_users():
    print(f"[{datetime.now()}] Cleaning up unverified users...")
    # Simulate cleanup
    # Imagine a DB query here to delete unverified users older than 7 days
