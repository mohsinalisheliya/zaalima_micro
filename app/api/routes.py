from fastapi import APIRouter, HTTPException
import uuid
from app.api.schemas import JobRequest, JobStatusResponse
from app.services.cache import set_job_status, get_job_status
from app.worker.tasks import process_video_task, process_image_task
from app.core.celery_app import celery_app

router = APIRouter()

@router.get("/health")
async def health_check():
    return {"status": "ok", "service": "media_processor"}

@router.post("/jobs")
async def submit_processing_job(job: JobRequest):
    job_id = str(uuid.uuid4())
    set_job_status(job_id, "pending")
    
    try:
        if "video" in job.task_type.lower():
            process_video_task.delay(job_id, job.filename, job.task_type, job.webhook_url)
        else:
            process_image_task.delay(job_id, job.filename, job.task_type, job.webhook_url)
    except Exception as e:
        set_job_status(job_id, "failed")
        raise HTTPException(status_code=500, detail="Message broker unavailable. Task failed.")
        
    return {"job_id": job_id, "status": "pending", "task": job.task_type}

@router.get("/jobs/{job_id}", response_model=JobStatusResponse)
async def get_job(job_id: str):
    data = get_job_status(job_id)
    if not data:
        raise HTTPException(status_code=404, detail="Job not found")
    return data

@router.delete("/jobs/{job_id}")
async def cancel_processing_job(job_id: str):
    job_data = get_job_status(job_id)
    if not job_data:
        raise HTTPException(status_code=404, detail="Job not found")
        
    if job_data["status"] in ["completed", "failed"]:
        raise HTTPException(status_code=400, detail="Cannot cancel a finished job")
        
    set_job_status(job_id, "cancelled")
    return {"job_id": job_id, "status": "cancelled", "message": "Job successfully cancelled"}

@router.post("/jobs/{job_id}/reset")
async def reset_failed_job(job_id: str):
    job_data = get_job_status(job_id)
    if not job_data:
        raise HTTPException(status_code=404, detail="Job not found")
        
    if job_data["status"] != "failed":
        raise HTTPException(status_code=400, detail="Only failed jobs can be manually reset")
        
    set_job_status(job_id, "pending")
    return {"job_id": job_id, "status": "pending", "message": "Job status reset successfully."}

@router.get("/workers/status")
async def get_worker_status():
    try:
        inspector = celery_app.control.inspect()
        active_workers = inspector.active()
        
        if not active_workers:
            return {"status": "warning", "message": "No active Celery workers found."}
            
        return {"status": "ok", "active_workers": active_workers}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Broker connection error: {str(e)}")