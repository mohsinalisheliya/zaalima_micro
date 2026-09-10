from pydantic import BaseModel

class JobRequest(BaseModel):
    filename: str
    task_type: str
    webhook_url: str | None = None

class JobStatusResponse(BaseModel):
    job_id: str
    status: str
    progress: int = 0
    result_url: str | None = None

class PresignRequest(BaseModel):
    filename: str

class PresignResponse(BaseModel):
    upload_url: str
    object_name: str