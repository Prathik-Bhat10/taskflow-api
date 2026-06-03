from fastapi import FastAPI
from app.routers import tasks
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

@app.get("/")
def home():
    return {
        "message": f"{settings.app_name} is running!",
        "version": settings.app_version
    }

app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])