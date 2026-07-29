# 🚀 Distributed Media Processing Microservice

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
* **Kamlesh** - Schemas, Utilities, & Image Processing Developer

---

## ⚙️ Prerequisites
Before running this project, ensure you have the following installed globally on your system:
1. **Python 3.10+**
2. **Docker Desktop** (Required for Redis & RabbitMQ)
3. **FFmpeg** (Required for video processing in Week 3)
4. **Git**

---

## 💻 Local Setup Instructions

**1. Clone the repository:**
```bash
git clone [https://github.com/mohsinalisheliya/zaalima_micro.git](https://github.com/mohsinalisheliya/zaalima_micro.git)
cd zaalima_micro