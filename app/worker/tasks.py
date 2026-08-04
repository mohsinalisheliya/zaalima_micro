from app.core.celery_app import celery_app
from app.services.cache import set_job_status
from app.services.aws_client import check_file_exists
import time

@celery_app.task(name="process_media_task")
def process_media_task(job_id: str, filename: str, task_type: str):
    logger.info(f"Worker picked up job {job_id} for file {filename}")
    # 1. Verify file exists in S3
    if not check_file_exists(filename):
        logger.error(f"File {filename} not found in S3 bucket.")
        set_job_status(job_id, "failed")
        return {"job_id": job_id, "status": "failed", "error": "File not found in S3"}
    # 2. Mark as processing
    set_job_status(job_id, "processing")
    # 3. Simulate heavy processing
    time.sleep(5)
    # 4. Mark as completed
    result_url = f"https://fake-cdn.com/{filename}"
    set_job_status(job_id, "completed", result_url=result_url)
    logger.info(f"Worker completed job {job_id}")
    return {"job_id": job_id, "status": "completed"}

