import requests

BASE_URL = "http://127.0.0.1:8000/api/v1"

print("Health:", requests.get(f"{BASE_URL}/health").json())
print("Submit Job:", requests.post(f"{BASE_URL}/jobs", json={"filename":"video.mp4", "task_type":"compress"}).json())
