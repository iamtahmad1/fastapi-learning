# app/celery_worker.py
from celery import Celery

celery_app = Celery(
    "worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1",
    include=["app.tasks"]  # 👈 include task module
)

celery_app.conf.timezone = 'UTC'

celery_app.conf.beat_schedule = {
    'cleanup-every-day': {
        'task': 'app.tasks.cleanup_unverified_users',
        'schedule': 86400.0,  # every 24 hours (can also use crontab)
    }
}
