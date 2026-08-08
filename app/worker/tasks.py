from app.core.celery_app import celery_app
from app.services.cache import set_job_status, update_job_progress
from app.services.aws_client import check_file_exists
import time
import random
import logging

logger = logging.getLogger(__name__)

@celery_app.task(name="process_image_task", bind=True, acks_late=True)
def process_image_task(self, job_id: str, filename: str, task_type: str):
    logger.info(f"[IMAGE QUEUE] Worker picked up job {job_id} for file {filename}")
    
    if not check_file_exists(filename):
        logger.error(f"File {filename} not found in S3 bucket.")
        set_job_status(job_id, "failed")
        return {"job_id": job_id, "status": "failed", "error": "File not found in S3"}

    set_job_status(job_id, "processing")
    time.sleep(2) # Simulating faster image resizing
    
    result_url = f"https://fake-cdn.com/image/{filename}"
    set_job_status(job_id, "completed", result_url=result_url)
    logger.info(f"[IMAGE QUEUE] Worker completed job {job_id}")
    
    return {"job_id": job_id, "status": "completed"}

