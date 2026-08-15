import json
from app.core.redis_client import redis_db

def set_job_status(job_id: str, status: str, result_url: str = None):
    data = {"job_id": job_id, "status": status}
    if result_url:
        data["result_url"] = result_url
        
    # Preserve progress if it exists
    existing = get_job_status(job_id)
    if existing and "progress" in existing:
        data["progress"] = existing["progress"]
        
    redis_db.setex(f"job:{job_id}", 86400, json.dumps(data))

def get_job_status(job_id: str):
    data = redis_db.get(f"job:{job_id}")
    if data:
        return json.loads(data)
    return None
    
def update_job_progress(job_id: str, progress: int):
    try:
        data = get_job_status(job_id)
        if data:
            data["progress"] = progress
            redis_db.setex(f"job:{job_id}", 86400, json.dumps(data))
    except Exception as e:
        print(f"Redis Error updating progress: {e}")

def clean_stale_redis_jobs():
    """Finds jobs stuck in processing for too long and marks them as failed."""
    try:
        for key in redis_db.scan_iter("job:*"):
            job_data = redis_db.get(key)
            if job_data:
                data = json.loads(job_data)
                if data.get("status") == "processing":
                    job_id = data.get("job_id")
                    set_job_status(job_id, "failed", result_url="Job timed out and was killed by system cleanup")
    except Exception as e:
        print(f"Redis Cleanup Error: {e}")