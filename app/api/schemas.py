from pydantic import BaseModel
class JobRequest(BaseModel):
    filename: str
    task_type: str  # e.g., 'compress_video', 'resize_image'
