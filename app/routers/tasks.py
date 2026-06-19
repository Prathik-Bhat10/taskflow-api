from fastapi import APIRouter, HTTPException, Path, Query
from typing import Annotated, Optional, List
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskStatus, TaskPriority
from app.services.task_service import TaskService
from app.db.database import db

router = APIRouter()

# Initialize task service with database
task_service = TaskService(db)


@router.get(
    "/stats",
    summary="Get task statistics",
    description="Returns count of tasks by status"
)
def get_task_stats():
    """Get statistics about tasks grouped by status."""
    return task_service.get_task_stats()


@router.get("/", response_model=List[TaskResponse], summary="Get all tasks")
def get_all_tasks(
    status: Annotated[Optional[TaskStatus], Query(description="Filter by status")] = None,
    priority: Annotated[Optional[TaskPriority], Query(description="Filter by priority")] = None,
    skip: Annotated[int, Query(ge=0, description="Tasks to skip")] = 0,
    limit: Annotated[int, Query(ge=1, le=100, description="Max tasks to return")] = 10,
):
    """
    Get all tasks with optional filtering by status and priority.

    - **status**: Filter by task status (pending, in_progress, done)
    - **priority**: Filter by task priority (low, medium, high)
    - **skip**: Number of tasks to skip for pagination
    - **limit**: Maximum number of tasks to return (max 100)
    """
    status_value = status.value if status else None
    priority_value = priority.value if priority else None
    return task_service.get_all_tasks(
        status=status_value,
        priority=priority_value,
        skip=skip,
        limit=limit
    )


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: Annotated[int, Path(gt=0, description="Task ID")]):
    """
    Get a specific task by ID.

    - **task_id**: The ID of the task to retrieve
    """
    task = task_service.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
    return task


@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(task: TaskCreate):
    """
    Create a new task.

    - **title**: Task title (required, 3-100 characters)
    - **description**: Task description (optional, max 500 characters)
    - **status**: Task status (pending, in_progress, done) - defaults to pending
    - **priority**: Task priority (low, medium, high) - defaults to medium
    - **due_date**: Task due date (optional, must be future date for high priority)
    - **tags**: Task tags (optional, max 5 tags)
    """
    return task_service.create_task(task)


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: Annotated[int, Path(gt=0, description="Task ID")],
    updated: TaskUpdate
):
    """
    Update an entire task (PUT - all fields).

    - **task_id**: The ID of the task to update
    - All fields in the request body are treated as replacements
    """
    task = task_service.update_task(task_id, updated)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
    return task


@router.patch("/{task_id}", response_model=TaskResponse)
def partial_update_task(
    task_id: Annotated[int, Path(gt=0, description="Task ID")],
    updated: TaskUpdate
):
    """
    Partially update a task (PATCH - only provided fields).

    - **task_id**: The ID of the task to update
    - Only fields provided in the request body are updated
    """
    task = task_service.update_task(task_id, updated)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
    return task


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: Annotated[int, Path(gt=0, description="Task ID")]):
    """
    Delete a task by ID.

    - **task_id**: The ID of the task to delete
    """
    deleted = task_service.delete_task(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
