"""
Task model for database representation using SQLModel.
SQLModel combines SQLAlchemy ORM with Pydantic validation.
"""
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone
import json
 
def _now() -> datetime:
    return datetime.now(timezone.utc)


class Task(SQLModel, table=True):
    """Task model representing a task record in the database."""
    
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: Optional[str] = None
    status: str = Field(default="pending", index=True)
    priority: str = Field(default="medium", index=True)
    due_date: Optional[datetime] = None
    tags: Optional[str] = None
    created_at: Optional[datetime] = Field(default_factory=_now)
    updated_at: Optional[datetime] = Field(default_factory=_now)

    def to_dict(self) -> dict:
        """Convert Task instance to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
            "due_date": self.due_date,
            "tags": json.loads(self.tags) if self.tags else [],
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def __repr__(self) -> str:
        return f"Task(id={self.id}, title={self.title}, status={self.status})"
