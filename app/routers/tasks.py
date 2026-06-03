from fastapi import APIRouter, HTTPException, Path, Query
from typing import Annotated, Optional, List
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskStatus, TaskPriority

router = APIRouter()

fake_tasks = [
    {"id": 1, "title": "Buy groceries", "description": "Milk and eggs", "status": "pending", "priority": "low", "due_date": None, "tags": ["personal"]},
    {"id": 2, "title": "Read FastAPI docs", "description": None, "status": "done", "priority": "medium", "due_date": None, "tags": ["learning"]},
    {"id": 3, "title": "Build TaskFlow API", "description": "Main project", "status": "in_progress", "priority": "high", "due_date": "2027-01-01T00:00:00Z", "tags": ["work", "urgent"]},
]

# ── specific routes first ──────────────────────────────────

@router.get(
    "/stats",
    summary="Get task statistics",
    description="Returns count of tasks by status"
)
def get_task_stats():
    total = len(fake_tasks)
    done = len([t for t in fake_tasks if t["status"] == "done"])
    pending = len([t for t in fake_tasks if t["status"] == "pending"])
    in_progress = len([t for t in fake_tasks if t["status"] == "in_progress"])
    return {"total": total, "done": done, "pending": pending, "in_progress": in_progress}

@router.get("/", response_model=List[TaskResponse], summary="Get all tasks")
def get_all_tasks(
    status: Annotated[Optional[TaskStatus], Query(description="Filter by status")] = None,
    priority: Annotated[Optional[TaskPriority], Query(description="Filter by priority")] = None,
    skip: Annotated[int, Query(ge=0, description="Tasks to skip")] = 0,
    limit: Annotated[int, Query(ge=1, le=100, description="Max tasks to return")] = 10,
):
    results = fake_tasks
    if status:
        results = [t for t in results if t["status"] == status]
    if priority:
        results = [t for t in results if t["priority"] == priority]
    return results[skip: skip + limit]

# ── dynamic routes after ───────────────────────────────────

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: Annotated[int, Path(gt=0, description="Task ID")],
    verbose: Annotated[bool, Query(description="Return extra debug info")] = False
):
    for task in fake_tasks:
        if task["id"] == task_id:
            if verbose:
                return {**task, "debug": "fetched from fake_tasks list"}
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(task: TaskCreate):
    new_task = {
        "id": len(fake_tasks) + 1,
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "priority": task.priority,
        "due_date": task.due_date,
        "tags": task.tags,
    }
    fake_tasks.append(new_task)
    return new_task

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: Annotated[int, Path(gt=0)],
    updated: TaskUpdate
):
    for task in fake_tasks:
        if task["id"] == task_id:
            if updated.title is not None:
                task["title"] = updated.title
            if updated.description is not None:
                task["description"] = updated.description
            if updated.status is not None:
                task["status"] = updated.status
            if updated.priority is not None:
                task["priority"] = updated.priority
            if updated.due_date is not None:
                task["due_date"] = updated.due_date
            if updated.tags is not None:
                task["tags"] = updated.tags
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@router.patch("/{task_id}", response_model=TaskResponse)
def partial_update_task(
    task_id: Annotated[int, Path(gt=0)],
    updated: TaskUpdate
):
    for task in fake_tasks:
        if task["id"] == task_id:
            update_data = updated.model_dump(exclude_unset=True)
            task.update(update_data)
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: Annotated[int, Path(gt=0)]):
    for i, task in enumerate(fake_tasks):
        if task["id"] == task_id:
            fake_tasks.pop(i)
            return
    raise HTTPException(status_code=404, detail="Task not found")