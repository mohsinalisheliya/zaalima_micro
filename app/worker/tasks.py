from app.core.celery_app import celery_app
from app.services.cache import set_job_status
from app.core.logger import logger
import time
@celery_app.task(name="process_media_task")
def process_media_task(job_id: str, filename: str, task_type: str):
    logger.info(f"Worker picked up job {job_id} for file {filename}")
    set_job_status(job_id, "processing")
    
    # Simulate heavy processing
    time.sleep(5)
    
    result_url = f"https://fake-cdn.com/{filename}"
    set_job_status(job_id, "completed", result_url=result_url)
    logger.info(f"Worker completed job {job_id}")
    return {"job_id": job_id, "status": "completed"}
