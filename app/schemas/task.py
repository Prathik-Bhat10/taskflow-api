from typing import Optional, Annotated
from pydantic import BaseModel, Field, field_validator, model_validator
from enum import Enum
from datetime import datetime, timezone

class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    done = "done"

class TaskPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

# Annotated types — define once, reuse anywhere
TaskTitle = Annotated[str, Field(min_length=3, max_length=100, description="Task title")]
TaskDescription = Annotated[Optional[str], Field(default=None, max_length=500)]
TagList = Annotated[Optional[list[str]], Field(default=[], max_length=5)]

class TaskCreate(BaseModel):
    title: TaskTitle
    description: TaskDescription = None
    status: TaskStatus = TaskStatus.pending
    priority: TaskPriority = TaskPriority.medium
    due_date: Optional[datetime] = None
    tags: TagList = []

    @field_validator("title")
    @classmethod
    def title_must_not_be_blank(cls, v):
        if v.strip() == "":
            raise ValueError("Title cannot be blank or just spaces")
        return v.strip()

    @field_validator("tags")
    @classmethod
    def tags_must_be_lowercase(cls, v):
        if v is None:
            return v
        return [tag.lower().strip() for tag in v]

    @field_validator("due_date")
    @classmethod
    def due_date_must_be_future(cls, v):
        if v is None:
            return v
        if v < datetime.now(timezone.utc):
            raise ValueError("due_date must be a future date")
        return v

    @model_validator(mode="after")
    def high_priority_needs_due_date(self):
        if self.priority == TaskPriority.high and self.due_date is None:
            raise ValueError("High priority tasks must have a due date")
        return self

class TaskUpdate(BaseModel):
    title: Optional[TaskTitle] = None
    description: TaskDescription = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None
    tags: TagList = None

    @field_validator("title")
    @classmethod
    def title_must_not_be_blank(cls, v):
        if v is not None and v.strip() == "":
            raise ValueError("Title cannot be blank or just spaces")
        return v.strip() if v else v

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: TaskStatus
    priority: TaskPriority
    due_date: Optional[datetime] = None
    tags: Optional[list[str]] = []

    class Config:
        from_attributes = True