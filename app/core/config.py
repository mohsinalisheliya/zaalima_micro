from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Media Processing Service"
    AWS_REGION: str = "us-east-1"

    class Config:
        env_file = ".env"

settings = Settings()