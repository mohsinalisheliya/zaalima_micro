import requests
import time
BASE_URL = "http://127.0.0.1:8000/api/v1"
print("--- 1. Submitting Video Job ---")
response = requests.post(f"{BASE_URL}/jobs", json={"filename": "test_video.mp4", "task_type": "compress_video"})
job_data = response.json()
job_id = job_data["job_id"]
print(f"Job Created: {job_id}")
print("\n--- 2. Polling for Live Progress ---")
while True:
    status_response = requests.get(f"{BASE_URL}/jobs/{job_id}").json()
    status = status_response.get("status")
    progress = status_response.get("progress", 0)
    print(f"Status: {status.upper()} | Progress: {progress}%")
    if status == "completed":
        print(f"✅ Success! Result URL: {status_response.get('result_url')}")
        break
    elif status == "failed":
        print("❌ Job Permanently Failed (Max retries exceeded).")
        break
    elif status == "retrying":
        print("⚠️ Network error detected. Worker is waiting 5 seconds to retry...")
        
    time.sleep(1) # Poll every 1 second
