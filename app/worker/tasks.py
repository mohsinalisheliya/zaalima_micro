from app.core.celery_app import celery_app
from app.services.cache import set_job_status
import time

@celery_app.task(name="process_media_task")
def process_media_task(job_id: str, filename: str, task_type: str):
    # 1. Mark as processing
    set_job_status(job_id, "processing")
    
    # 2. Simulate a heavy 5-second task (we will replace this with real video/image processing next week)
    time.sleep(5)
    
    # 3. Mark as completed
    result_url = f"https://fake-cdn.com/{filename}"
    set_job_status(job_id, "completed", result_url=result_url)
    
    return {"job_id": job_id, "status": "completed"}
