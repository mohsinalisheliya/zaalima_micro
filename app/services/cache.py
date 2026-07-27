from app.core.redis_client import get_redis_client
import json

redis_db = get_redis_client()
def get_job_status(job_id: str) -> dict:
    data = redis_db.get(f"job:{job_id}")
    if data:
        return json.loads(data)
    return None

