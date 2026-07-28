# Wrap getter in try-except
def get_job_status(job_id: str) -> dict:
    try:
        data = redis_db.get(f"job:{job_id}")
        return json.loads(data) if data else None
    except Exception as e:
        print(f"Redis Error: {e}")
        return None
