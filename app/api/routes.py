from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health_check():
    return {"status": "ok", "service": "media_processor"}

@router.post("/upload-url")
async def request_upload_url(filename: str):
    # Logic will be connected to the AWS client tomorrow
    return {"filename": filename, "upload_url": "pending_implementation"}