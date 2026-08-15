from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Distributed Media Processing"
    
    # Week 1
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_BUCKET_NAME: str
    AWS_REGION: str = "us-east-1"
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    
    # Week 2
    CELERY_BROKER_URL: str = "amqp://guest:guest@localhost:5672//"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    CELERY_TASK_TIME_LIMIT: int = 300
    CELERY_TASK_SOFT_TIME_LIMIT: int = 240
    CELERY_DEFAULT_QUEUE: str = "default_media_queue"
    CELERY_IMAGE_QUEUE: str = "image_processing"
    CELERY_VIDEO_QUEUE: str = "video_processing"
    CELERY_WORKER_PREFETCH_MULTIPLIER: int = 1
    FLOWER_PORT: int = 5555
    CELERY_ENABLE_FLOWER: bool = True
    CELERY_TASK_MAX_RETRIES: int = 3
    CELERY_TASK_RETRY_DELAY: int = 5
    
    # Week 3
    IMAGE_MAX_RESOLUTION: tuple = (1080, 1080)
    IMAGE_QUALITY_PERCENT: int = 85
    VIDEO_MAX_RESOLUTION: str = "1280x720"
    VIDEO_CODEC: str = "libx264"
    AWS_GET_EXPIRE_SECONDS: int = 86400
    WEBHOOK_TIMEOUT_SECONDS: int = 5

    class Config:
        env_file = ".env"

settings = Settings()