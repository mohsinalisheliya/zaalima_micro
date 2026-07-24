from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    PROJECT_NAME: str = "Media Processing Service"
    AWS_REGION: str = "us-east-1
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_BUCKET_NAME: str = "my-media-bucket"

    class Config:
        env_file = ".env"
settings = Settings()
class Settings(BaseSettings):
    APP_NAME: str = "Zaalima"
    AWS_REGION: str = "ap-south-1"

    PRESIGNED_URL_EXPIRE_SECONDS: int = 3600git status