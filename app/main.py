from fastapi import FastAPI
from app.api.routes import router
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

# Include API routes
app.include_router(router, prefix="/api/v1")
