from pydantic import BaseModel
class JobRequest(BaseModel):
    filename: str
    task_type: str  # e.g., 'compress_video', 'resize_image'
class JobStatusResponse(BaseModel):
    job_id: str
    status: str
    result_url: str | None = None
