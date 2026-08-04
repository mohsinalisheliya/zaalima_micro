from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "media_processor",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.worker.tasks"]
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_acks_late=True,  # Don't acknowledge until task is fully complete
    task_routes={
        'process_video_task': {'queue': settings.CELERY_VIDEO_QUEUE},
        'process_image_task': {'queue': settings.CELERY_IMAGE_QUEUE},
    }
)
