# 🚀 Distributed Media Processing Microservices

An asynchronous, event-driven backend microservice designed to handle heavy media workloads. This system securely offloads CPU-intensive tasks (like image resizing and video transcoding) from the main web application to background workers, ensuring high performance and a non-blocking user experience.

## 🛠️ Tech Stack
* **Web Framework:** FastAPI (Python)
* **Asynchronous Task Queue:** Celery
* **Message Broker:** RabbitMQ
* **Caching Layer:** Redis
* **Cloud Storage:** AWS S3 (via Boto3)
* **Media Processing:** Pillow (Images), FFmpeg (Video)
* **Infrastructure:** Docker & Docker Compose

---
## �️ Fault Tolerance & Retries
This system features automatic task retries. If a worker encounters a temporary network error (like an S3 timeout), it will not fail the job immediately. Instead, it will automatically wait 5 seconds and retry the task up to 3 times before marking it as permanently failed. Clients can poll the status endpoint and will see the status temporarily change to `"retrying"`.

---

## �👥 The Team (Zaalima Micro)
* **Mohsin Ali** - Team Leader & Orchestrator
* **Haana Farook** - API & Routes Developer
* **Sidram** - Core Configuration & Middleware Developer
* **Raghuwansan** - Cloud Infrastructure & Video Processing Developer
* **Kamalesh** - Schemas, Utilities, & Image Processing Developer

---

## ⚙️ Prerequisites
Before running this project, ensure you have the following installed globally on your system:
1. **Python 3.10+**
2. **Docker Desktop** (Required for Redis & RabbitMQ)
3. **FFmpeg** (Required for video processing in Week 3)
4. **Git**

## 🎬 Video Processing
Prerequisites (Week 3)

To process videos, you must have FFmpeg installed globally on your system.

* **Windows:** Download the FFmpeg essentials build, extract it, and add the `bin` folder to your global Windows System Environment Variables.
* Do not attempt to install this inside your local Python environment; the core dependency must remain accessible via a global path.

---

💻 Running the Application Locally

Open FOUR separate terminal windows and run these commands:

**Terminal 1 (Infrastructure):**
`docker-compose up -d`

**Terminal 2 (FastAPI Server):**
`uvicorn app.main:app --reload`

**Terminal 3 (Video Worker):**
*Mac/Linux:* `celery -A app.core.celery_app.celery_app worker -Q video_processing --loglevel=info`
*Windows:* `celery -A app.core.celery_app.celery_app worker -Q video_processing --loglevel=info --pool=solo`

**Terminal 4 (Image Worker):**
*Mac/Linux:* `celery -A app.core.celery_app.celery_app worker -Q image_processing --loglevel=info`
*Windows:* `celery -A app.core.celery_app.celery_app worker -Q image_processing --loglevel=info --pool=solo`

**Terminal 5 (Celery Flower Monitor):**
`celery -A app.core.celery_app.celery_app flower --port=5555`

*Once Flower is running, open your browser and go to `http://localhost:5555` to visually monitor all active, pending, and failed queues.*

---

## 💻 Local Setup Instructions

**1. Clone the repository:**
```bash
git clone [https://github.com/mohsinalisheliya/zaalima_micro.git](https://github.com/mohsinalisheliya/zaalima_micro.git)
cd zaalima_micro
