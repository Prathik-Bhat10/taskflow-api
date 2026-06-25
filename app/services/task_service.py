"""
Task service layer - Business logic for task operations.
This layer handles all task-related operations and acts as an intermediary
between the routers and the database.
"""
from typing import List, Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from sqlalchemy import func
from datetime import datetime, timezone
import json


def _now() -> datetime:
    return datetime.now(timezone.utc)


class TaskService:
    """Service class for task operations."""

    def __init__(self, session: AsyncSession):
        """
        Initialize TaskService with a database session.

        Args:
            session: SQLAlchemy AsyncSession instance
        """
        self.session = session

    async def create_task(self, task_create: TaskCreate) -> TaskResponse:
        """
        Create a new task in the database.

        Args:
            task_create: TaskCreate schema with task data

        Returns:
            TaskResponse with created task data
        """
        tags_json = json.dumps(task_create.tags) if task_create.tags is not None else None

        task = Task(
            title=task_create.title,
            description=task_create.description,
            status=task_create.status.value,
            priority=task_create.priority.value,
            due_date=task_create.due_date,
            tags=tags_json,
            created_at=_now(),
            updated_at=_now(),
        )

        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)

        return TaskResponse(**task.to_dict())

    async def get_task(self, task_id: int) -> Optional[TaskResponse]:
        """
        Retrieve a specific task by ID.

        Args:
            task_id: ID of the task

        Returns:
            TaskResponse if found, None otherwise
        """
        task = await self.session.get(Task, task_id)
        if not task:
            return None

        return TaskResponse(**task.to_dict())

    async def get_all_tasks(
        self,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        skip: int = 0,
        limit: int = 10,
    ) -> List[TaskResponse]:
        """
        Retrieve all tasks with optional filtering.

        Args:
            status: Filter by status
            priority: Filter by priority
            skip: Number of tasks to skip
            limit: Maximum number of tasks to return

        Returns:
            List of TaskResponse objects
        """
        query = select(Task)

        if status:
            query = query.where(Task.status == status)
        if priority:
            query = query.where(Task.priority == priority)

        query = query.offset(skip).limit(limit)
        result = await self.session.exec(query)
        tasks = result.all()

        return [TaskResponse(**task.to_dict()) for task in tasks]

    async def replace_task(self, task_id: int, task_update: TaskUpdate) -> Optional[TaskResponse]:
        task = await self.session.get(Task, task_id)
        if not task:
            return None

        task.title = task_update.title or task.title  # keep existing if None
        task.status = (task_update.status.value if task_update.status is not None else task.status)
        task.priority = (task_update.priority.value if task_update.priority is not None else task.priority)
        task.description = task_update.description  
        task.due_date = task_update.due_date
        task.tags = json.dumps(task_update.tags) if task_update.tags is not None else None
        task.updated_at = _now()

        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)

        return TaskResponse(**task.to_dict())

    async def update_task(self, task_id: int, task_update: TaskUpdate) -> Optional[TaskResponse]:
        """
        Partially update an existing task (PATCH semantics — only provided fields).

        Args:
            task_id: ID of the task to update
            task_update: TaskUpdate schema with fields to update

        Returns:
            Updated TaskResponse if successful, None if task not found
        """
        task = await self.session.get(Task, task_id)
        if not task:
            return None

        if task_update.title is not None:
            task.title = task_update.title
        if task_update.description is not None:
            task.description = task_update.description
        if task_update.status is not None:
            task.status = task_update.status.value
        if task_update.priority is not None:
            task.priority = task_update.priority.value
        if task_update.due_date is not None:
            task.due_date = task_update.due_date
        if task_update.tags is not None:
            task.tags = json.dumps(task_update.tags)

        task.updated_at = _now()
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)

        return TaskResponse(**task.to_dict())

    async def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by ID.

        Args:
            task_id: ID of the task to delete

        Returns:
            True if deleted, False if not found
        """
        task = await self.session.get(Task, task_id)
        if not task:
            return False

        await self.session.delete(task)
        await self.session.commit()
        return True

    async def get_task_stats(self) -> dict:
        """
        Get statistics about tasks grouped by status.

        Returns:
            Dictionary with task counts by status
        """
        result = await self.session.exec(
            select(Task.status, func.count()).group_by(Task.status)
        )
        stats = {
            "total": 0,
            "pending": 0,
            "in_progress": 0,
            "done": 0,
        }

        for status, count in result:
            if status in stats:
                stats[status] = count
            stats["total"] += count

        return stats