import requests
import time

BASE_URL = "http://127.0.0.1:8000/api/v1"

print("--- Submitting Multiple Jobs to the Queue ---")
for i in range(1, 6):
    payload = {"filename": f"video_{i}.mp4", "task_type": "compress"}
    response = requests.post(f"{BASE_URL}/jobs", json=payload)
    print(f"Job {i}:", response.json())
    
print("\n--- Check the Celery terminal! You should see it processing these one by one ---")
