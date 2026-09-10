import os
import random
from app.core.celery_app import celery_app
from app.core.config import settings
from app.core.logger import logger
from app.services.cache import set_job_status, update_job_progress, clean_stale_redis_jobs
from app.services.aws_client import check_file_exists, download_file_from_s3, upload_file_to_s3, generate_download_presigned_url
from app.utils.helpers import create_job_workspace, clear_local_workspaces
from app.services.image_ops import compress_and_resize_image
from app.services.video_ops import compress_video, extract_thumbnail
from app.services.webhook import send_webhook

@celery_app.task(name="process_video_task", bind=True, acks_late=True)
def process_video_task(self, job_id: str, filename: str, task_type: str, webhook_url: str = None):
    logger.info(f"[VIDEO QUEUE] Worker picked up job {job_id} for file {filename}")
    
    if not check_file_exists(filename):
        logger.error(f"File {filename} not found in S3 bucket.")
        set_job_status(job_id, "failed")
        return {"job_id": job_id, "status": "failed", "error": "File not found in S3"}

    set_job_status(job_id, "processing")
    update_job_progress(job_id, 10) 

    workspace = create_job_workspace(job_id)
    # Sanitize paths: forcefully convert any Windows backslashes to standard forward slashes
    input_path = os.path.join(workspace, filename).replace("\\", "/")
    processed_filename = f"processed_{filename}"
    output_path = os.path.join(workspace, processed_filename).replace("\\", "/")

    # Simulated Network Failure with Auto-Retry
    if random.random() < 0.3:
        logger.warning(f"[VIDEO QUEUE] Simulated network timeout for job {job_id}. Retrying...")
        set_job_status(job_id, "retrying")
        raise self.retry(exc=Exception("Simulated connection lost"), countdown=settings.CELERY_TASK_RETRY_DELAY, max_retries=settings.CELERY_TASK_MAX_RETRIES)

    # 1. Download
    logger.info(f"Downloading {filename} for job {job_id}")
    if not download_file_from_s3(filename, input_path):
        raise self.retry(exc=Exception("Failed to download video"), countdown=5, max_retries=3)
    update_job_progress(job_id, 40)

    # 2. Process Video
    logger.info(f"Compressing video for job {job_id}")
    if not compress_video(input_path, output_path):
        set_job_status(job_id, "failed", result_url="FFmpeg Processing Error")
        return {"job_id": job_id, "status": "failed"}
    update_job_progress(job_id, 80)

    # 3. Upload
    logger.info(f"Uploading processed video for job {job_id}")
    s3_key = f"processed/video/{processed_filename}"
    if not upload_file_to_s3(output_path, s3_key):
        raise self.retry(exc=Exception("Failed to upload processed video"), countdown=5, max_retries=3)
    
    update_job_progress(job_id, 100)
    
    secure_result_url = generate_download_presigned_url(s3_key)
    set_job_status(job_id, "completed", result_url=secure_result_url)
    
    if webhook_url:
        send_webhook(webhook_url, job_id, "completed", secure_result_url)
    
    # 4. Cleanup local files
    try:
        os.remove(input_path)
        os.remove(output_path)
    except Exception as e:
        logger.warning(f"Failed to cleanup workspace for {job_id}: {e}")

    logger.info(f"[VIDEO QUEUE] Worker completed job {job_id}")
    return {"job_id": job_id, "status": "completed"}

@celery_app.task(name="process_image_task", bind=True, acks_late=True)
def process_image_task(self, job_id: str, filename: str, task_type: str, webhook_url: str = None):
    logger.info(f"[IMAGE QUEUE] Worker picked up job {job_id} for file {filename}")
    
    if not check_file_exists(filename):
        logger.error(f"File {filename} not found in S3 bucket.")
        set_job_status(job_id, "failed")
        return {"job_id": job_id, "status": "failed", "error": "File not found in S3"}

    set_job_status(job_id, "processing")
    update_job_progress(job_id, 10) 

    workspace = create_job_workspace(job_id)
    # Sanitize paths: forcefully convert any Windows backslashes to standard forward slashes
    input_path = os.path.join(workspace, filename).replace("\\", "/")
    processed_filename = f"processed_{filename.rsplit('.', 1)[0]}.jpg"
    output_path = os.path.join(workspace, processed_filename).replace("\\", "/")

    # 1. Download
    logger.info(f"Downloading {filename} for job {job_id}")
    if not download_file_from_s3(filename, input_path):
        raise self.retry(exc=Exception("Failed to download image"), countdown=5, max_retries=3)
    update_job_progress(job_id, 40)

    # 2. Process
    logger.info(f"Compressing image for job {job_id}")
    if not compress_and_resize_image(input_path, output_path):
        set_job_status(job_id, "failed", result_url="Corrupt Image File")
        return {"job_id": job_id, "status": "failed"}
    update_job_progress(job_id, 70)

    # 3. Upload
    logger.info(f"Uploading processed image for job {job_id}")
    s3_key = f"processed/image/{processed_filename}"
    if not upload_file_to_s3(output_path, s3_key):
        raise self.retry(exc=Exception("Failed to upload processed image"), countdown=5, max_retries=3)
    
    update_job_progress(job_id, 100)
    
    secure_result_url = generate_download_presigned_url(s3_key)
    set_job_status(job_id, "completed", result_url=secure_result_url)
    
    if webhook_url:
        send_webhook(webhook_url, job_id, "completed", secure_result_url)
    
    # 4. Cleanup local files
    try:
        os.remove(input_path)
        os.remove(output_path)
    except Exception as e:
        logger.warning(f"Failed to cleanup workspace for {job_id}: {e}")

    logger.info(f"[IMAGE QUEUE] Worker completed job {job_id}")
    return {"job_id": job_id, "status": "completed"}

@celery_app.task(name="system_maintenance_task")
def system_maintenance_task():
    logger.info("[MAINTENANCE] Starting routine system cleanup...")
    
    # Clean local hard drive
    deleted_folders = clear_local_workspaces(max_age_hours=24)
    logger.info(f"[MAINTENANCE] Deleted {deleted_folders} old workspace folders.")
    
    # Clean Redis
    clean_stale_redis_jobs()
    logger.info("[MAINTENANCE] Redis stale job sweep complete.")
    
    return {"status": "success", "deleted_folders": deleted_folders}