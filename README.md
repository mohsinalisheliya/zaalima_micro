# Distributed Media Processing Microservice

An asynchronous, event-driven backend microservice designed to handle heavy media workloads using FastAPI, Celery, RabbitMQ, Redis, and AWS S3.

## 🛠️ Complete System Launch (One-Click)

This project is fully containerized. You do not need to install FFmpeg or Python on your local machine to run it.

**1 Create your environment file:**

Ensure you have a `.env` file in the root directory with your AWS keys:

```env
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_BUCKET_NAME=your_bucket
AWS_REGION=us-east-1
CELERY_BROKER_URL=amqp://guest:guest@rabbitmq:5672//
CELERY_RESULT_BACKEND=redis://redis:6379/0
REDIS_HOST=redis
REDIS_PORT=6379
```

**2. Start the entire microservice architecture:**

```bash
docker-compose up --build
```

*This single command boots the Redis Cache, RabbitMQ Broker, FastAPI Server, Video Celery Worker, and Image Celery Worker.*

**3. Access the Application:**

- API Swagger UI: http://localhost:8000/docs
- RabbitMQ Dashboard: http://localhost:15672 (guest/guest)
