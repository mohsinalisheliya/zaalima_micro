import requests
from app.core.config import settings

def send_webhook(webhook_url: str, job_id: str, status: str, result_url: str = None):
    """Fires a POST request to the client's webhook URL with the job results."""
    if not webhook_url:
        return False
        
    payload = {
        "job_id": job_id,
        "status": status,
        "result_url": result_url
    }
    
    try:
        response = requests.post(
            webhook_url, 
            json=payload, 
            timeout=settings.WEBHOOK_TIMEOUT_SECONDS
        )
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"Webhook Dispatch Error for Job {job_id}: {e}")
        return False