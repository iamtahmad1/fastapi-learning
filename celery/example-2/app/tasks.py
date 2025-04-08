# app/tasks.py
from celery import shared_task
from datetime import datetime

@shared_task
def cleanup_expired_sessions():
    print(f"[{datetime.now()}] ⏳ Cleaning up expired sessions...")
