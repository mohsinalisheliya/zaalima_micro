from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Media Processing Service"
    AWS_REGION: str = "us-east-1"
    CELERY_BROKER_URL: str = "amqp://guest:guest@localhost:5672//"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    CELERY_VIDEO_QUEUE: str = "video_processing"
    CELERY_IMAGE_QUEUE: str = "image_processing"

    class Config:
        env_file = ".env"


settings = Settings()