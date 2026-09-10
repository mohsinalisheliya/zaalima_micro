# Distributed Media Processing Microservice [zaalima Development]

An asynchronous, event-driven backend microservice designed to handle heavy media workloads using FastAPI, Celery, RabbitMQ, Redis, and AWS S3.

## 🛠️ Complete System Launch

This project is fully containerized. You do not need to install FFmpeg or Python on your local machine to run it.

**1. Create your environment file:**

Copy `.env.example` to `.env` and fill in your real AWS keys:
```bash
cp .env.example .env
```
```env
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_BUCKET_NAME=your_bucket
AWS_REGION=us-east-1
REDIS_HOST=redis
REDIS_PORT=6379
CELERY_BROKER_URL=amqp://guest:guest@rabbitmq:5672//
CELERY_RESULT_BACKEND=redis://redis:6379/0
```

**2. Start the entire microservice architecture:**

```bash
docker-compose up --build
```

*This single command boots the Redis Cache, RabbitMQ Broker, FastAPI Server, Video Celery Worker, Image Celery Worker, Celery Beat (scheduled maintenance), and the Flower monitoring dashboard.*

**3. Access the Application:**

- API Swagger UI: http://localhost:8000/docs
- RabbitMQ Dashboard: http://localhost:15672 (guest/guest)
- Flower (Celery task monitor): http://localhost:5555

## 📦 API Workflow

1. **Request an upload URL** — `POST /api/v1/uploads/presign` with `{"filename": "myvideo.mp4"}`. Returns a secure, time-limited S3 `upload_url` plus the generated `object_name`.
2. **Upload directly to S3** — `PUT` your file's bytes to `upload_url` from the client (browser/app), bypassing the API server entirely.
3. **Submit a processing job** — `POST /api/v1/jobs` with `{"filename": "<object_name from step 1>", "task_type": "compress_video", "webhook_url": "optional"}`.
4. **Poll for status** — `GET /api/v1/jobs/{job_id}` returns `status`, `progress`, and (once done) a presigned `result_url` you can download directly.
5. Optionally cancel a pending job (`DELETE /api/v1/jobs/{job_id}`) or reset a failed one (`POST /api/v1/jobs/{job_id}/reset`).

`task_type` containing `"video"` is routed to the video queue/worker (FFmpeg compression + thumbnailing); anything else is routed to the image queue/worker (Pillow resize/compress).

## ✅ What was fixed to complete this project

The repository was left mid-build with several broken links between modules. These have been resolved:

- **`app/core/redis_client.py`** — didn't expose the `redis_db` object that `app/services/cache.py` imported; added a shared, module-level Redis connection.
- **`app/services/aws_client.py`** — `get_s3_client()` built an unauthenticated boto3 client (the credentialed version was unreachable dead code after an early `return`); also added the missing `generate_download_presigned_url()` used by the workers to hand back a secure result link.
- **`app/services/weebhook.py` → `app/services/webhook.py`** — renamed to match the import used in `app/worker/tasks.py` (`from app.services.webhook import send_webhook`).
- **`app/core/config.py`** — added the missing `PRESIGNED_URL_EXPIRE_SECONDS` setting that `aws_client.py` referenced but never defined.
- **`app/api/routes.py` / `app/api/schemas.py`** — added the missing `POST /api/v1/uploads/presign` endpoint. Without it, there was no way for a client to actually get an S3 upload URL before submitting a job.
- **`app/core/celery_app.py` + `docker-compose.yml`** — wired up a Celery Beat schedule so the already-written `system_maintenance_task` (stale workspace/Redis cleanup) actually runs periodically, and added `worker_beat` and `flower` services to `docker-compose.yml`.
- **`requirements.txt`** — added `requests` (used by the webhook service) and `python-dotenv` (needed for `.env` loading).
- **`.gitignore`** — removed a stray leftover `Plaintext` line from a copy/paste.
- **`.env.example`** — expanded to include all variables the app actually reads (Redis/Celery/RabbitMQ), not just the AWS keys.

## 🧪 Smoke test

With the stack running:
```bash
python test_api.py
```
This submits a test video job and polls it to completion, printing live progress.
