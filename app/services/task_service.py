"""
Task service layer - Business logic for task operations.
This layer handles all task-related operations and acts as an intermediary
between the routers and the database.
"""
from typing import List, Optional
from app.db.database import Database
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse


class TaskService:
    """Service class for task operations."""

    def __init__(self, db: Database):
        """
        Initialize TaskService with a database instance.

        Args:
            db: Database instance
        """
        self.db = db

    def create_task(self, task_create: TaskCreate) -> TaskResponse:
        """
        Create a new task in the database.

        Args:
            task_create: TaskCreate schema with task data

        Returns:
            TaskResponse with created task data
        """
        tags_str = ",".join(task_create.tags) if task_create.tags else None

        task_id = self.db.add_task(
            title=task_create.title,
            description=task_create.description,
            status=task_create.status.value,
            priority=task_create.priority.value,
            due_date=task_create.due_date.isoformat() if task_create.due_date else None,
            tags=tags_str,
        )

        task = self.get_task(task_id)
        if task is None:
            raise RuntimeError(f"Failed to retrieve created task with id {task_id}")
        return task

    def get_task(self, task_id: int) -> Optional[TaskResponse]:
        """
        Retrieve a specific task by ID.

        Args:
            task_id: ID of the task

        Returns:
            TaskResponse if found, None otherwise
        """
        task_row = self.db.get_task(task_id)
        if not task_row:
            return None

        task = Task.from_db_row(task_row)
        return TaskResponse(**task.to_dict())

    def get_all_tasks(
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
        tasks_rows = self.db.get_tasks(status=status, priority=priority)

        tasks = [Task.from_db_row(row).to_dict() for row in tasks_rows]
        paginated = tasks[skip : skip + limit]

        return [TaskResponse(**task) for task in paginated]

    def update_task(self, task_id: int, task_update: TaskUpdate) -> Optional[TaskResponse]:
        """
        Update an existing task.

        Args:
            task_id: ID of the task to update
            task_update: TaskUpdate schema with fields to update

        Returns:
            Updated TaskResponse if successful, None if task not found
        """
        # Build update dictionary with only set fields
        update_data = {}

        if task_update.title is not None:
            update_data["title"] = task_update.title
        if task_update.description is not None:
            update_data["description"] = task_update.description
        if task_update.status is not None:
            update_data["status"] = task_update.status.value
        if task_update.priority is not None:
            update_data["priority"] = task_update.priority.value
        if task_update.due_date is not None:
            update_data["due_date"] = task_update.due_date.isoformat()
        if task_update.tags is not None:
            update_data["tags"] = ",".join(task_update.tags)

        if not update_data:
            return self.get_task(task_id)

        updated = self.db.update_task(task_id, **update_data)
        if not updated:
            return None

        return self.get_task(task_id)

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by ID.

        Args:
            task_id: ID of the task to delete

        Returns:
            True if deleted, False if not found
        """
        return self.db.delete_task(task_id)

    def get_task_stats(self) -> dict:
        """
        Get statistics about tasks grouped by status.

        Returns:
            Dictionary with task counts by status
        """
        all_tasks = self.db.get_tasks()

        stats = {
            "total": len(all_tasks),
            "pending": 0,
            "in_progress": 0,
            "done": 0,
        }

        for task in all_tasks:
            status = task[3]  # status is at index 3
            if status in stats:
                stats[status] += 1

        return stats
