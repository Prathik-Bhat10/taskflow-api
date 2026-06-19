"""
TaskFlow API - Main FastAPI application.

A RESTful API for task management with the following features:
- Create, Read, Update, Delete (CRUD) operations for tasks
- Task filtering by status and priority
- Task statistics
- Validation and error handling
- SQLite database integration
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.routers import tasks_router
from app.core.config import settings
from app.db.database import db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Connect to the database on startup and close it on shutdown."""
    db.connect()
    db.create_table()
    yield
    db.close()


# Create FastAPI application instance
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="A comprehensive task management API with full CRUD operations",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)


@app.get("/", tags=["Root"])
def home():
    """
    Root endpoint - API information.

    Returns:
        API name, version, and documentation links
    """
    return {
        "message": f"{settings.app_name} is running!",
        "version": settings.app_version,
        "docs": "/docs",
        "redoc": "/redoc",
    }


# Include routers
app.include_router(tasks_router, prefix="/tasks", tags=["Tasks"])
