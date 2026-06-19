"""
Task model for database representation.
This is the ORM-like layer that represents database records.
"""
from typing import Optional


class Task:
    """Task model representing a task record in the database."""

    def __init__(
        self,
        id: int,
        title: str,
        description: Optional[str] = None,
        status: str = "pending",
        priority: str = "medium",
        due_date: Optional[str] = None,
        tags: Optional[str] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
    ):
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.priority = priority
        self.due_date = due_date
        self.tags = tags
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def from_db_row(cls, row: tuple) -> "Task":
        """
        Create a Task instance from a database row.
        Supports both legacy 7-column rows and current 9-column rows.
        """
        status = cls._normalize_status(row[3])
        priority = cls._normalize_priority(row[4])

        base_kwargs = {
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "status": status,
            "priority": priority,
            "due_date": row[5],
            "tags": row[6],
        }

        if len(row) == 7:
            return cls(**base_kwargs)
        if len(row) == 9:
            return cls(
                **base_kwargs,
                created_at=row[7],
                updated_at=row[8],
            )
        raise ValueError(f"Unsupported task row shape: {len(row)} columns")

    @staticmethod
    def _normalize_status(value: str) -> str:
        if value is None:
            return "pending"
        normalized = value.strip().lower().replace(" ", "_")
        if normalized == "completed":
            return "done"
        return normalized

    @staticmethod
    def _normalize_priority(value: str) -> str:
        if value is None:
            return "medium"
        normalized = value.strip().lower()
        if normalized not in {"low", "medium", "high"}:
            return "medium"
        return normalized

    def to_dict(self) -> dict:
        """Convert Task instance to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
            "due_date": self.due_date,
            "tags": self.tags.split(",") if self.tags else [],
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def __repr__(self) -> str:
        return f"Task(id={self.id}, title={self.title}, status={self.status})"
