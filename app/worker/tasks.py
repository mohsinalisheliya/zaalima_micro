from app.core.celery_app import celery_app
from app.services.cache import set_job_status, update_job_progress
from app.services.aws_client import check_file_exists
import time
import logging

logger = logging.getLogger(__name__)

@celery_app.task(name="process_video_task", bind=True, acks_late=True)
def process_video_task(self, job_id: str, filename: str, task_type: str):
    logger.info(f"[VIDEO QUEUE] Worker picked up job {job_id} for file {filename}")

    if not check_file_exists(filename):
        logger.error(f"File {filename} not found in S3 bucket.")
        set_job_status(job_id, "failed")
        return {"job_id": job_id, "status": "failed", "error": "File not found in S3"}

    set_job_status(job_id, "processing")

    # Simulate heavy processing with progress updates
    for i in range(20, 101, 20):
        time.sleep(1)  # Processing chunk...
        update_job_progress(job_id, i)
        logger.info(f"[VIDEO QUEUE] Job {job_id} progress: {i}%")

    result_url = f"https://fake-cdn.com/video/{filename}"
    set_job_status(job_id, "completed", result_url=result_url)
    logger.info(f"[VIDEO QUEUE] Worker completed job {job_id}")
    return {"job_id": job_id, "status": "completed"}