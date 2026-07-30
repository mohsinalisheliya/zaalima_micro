from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "media_processor",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.worker.tasks"]
)

# Optional configuration for tasks
celery_app.conf.task_track_started = True
