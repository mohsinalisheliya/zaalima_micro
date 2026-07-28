# Wrap getter in try-except
def get_job_status(job_id: str) -> dict:
    try:
        data = redis_db.get(f"job:{job_id}")
        return json.loads(data) if data else None
    except Exception as e:
        print(f"Redis Error: {e}")
        return None

# Wrap setter in try-except
def set_job_status(job_id: str, status: str, result_url: str = None):
    try:
        data = {"status": status, "result_url": result_url}
        redis_db.setex(f"job:{job_id}", 86400, json.dumps(data))
    except Exception as e:
        print(f"Redis Error: {e}")
