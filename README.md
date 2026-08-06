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

## 👥 The Team (Zaalima Micro)
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

---

## 💻 Running the Application Locally

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

---

## 💻 Local Setup Instructions

**1. Clone the repository:**
```bash
git clone [https://github.com/mohsinalisheliya/zaalima_micro.git](https://github.com/mohsinalisheliya/zaalima_micro.git)
cd zaalima_micro
