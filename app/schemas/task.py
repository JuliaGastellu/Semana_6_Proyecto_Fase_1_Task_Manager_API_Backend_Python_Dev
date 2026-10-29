from datetime import date, datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, computed_field, field_validator

from app.schemas.category import CategorySummary


class TaskStatus(StrEnum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class TaskBase(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    title: str = Field(min_length=3, max_length=200, examples=["Revisar el PR de autenticación"])
    description: str | None = Field(default=None, max_length=1000)
    status: TaskStatus = TaskStatus.PENDING
    priority: int = Field(default=3, ge=1, le=5)
    due_date: date | None = None
    category_id: int | None = Field(default=None, gt=0)
    tags: list[str] = Field(default_factory=list, max_length=10)

    @field_validator("due_date")
    @classmethod
    def due_date_not_past(cls, value: date | None) -> date | None:
        if value is not None and value < date.today():
            raise ValueError("due_date no puede estar en el pasado")
        return value

    @field_validator("tags", mode="before")
    @classmethod
    def normalize_tags(cls, value: Any) -> Any:
        if not isinstance(value, list):
            return value
        return list(dict.fromkeys(str(item).strip().lower() for item in value if str(item).strip()))


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    title: str | None = Field(default=None, min_length=3, max_length=200)
    description: str | None = Field(default=None, max_length=1000)
    status: TaskStatus | None = None
    priority: int | None = Field(default=None, ge=1, le=5)
    due_date: date | None = None
    category_id: int | None = Field(default=None, gt=0)
    tags: list[str] | None = Field(default=None, max_length=10)

    @field_validator("title", "status", "priority", "tags")
    @classmethod
    def not_null(cls, value: Any) -> Any:
        if value is None:
            raise ValueError("no puede ser null: si no quiero cambiarlo, no lo envío")
        return value

    @field_validator("due_date")
    @classmethod
    def due_date_not_past(cls, value: date | None) -> date | None:
        if value is not None and value < date.today():
            raise ValueError("due_date no puede estar en el pasado")
        return value

    @field_validator("tags", mode="before")
    @classmethod
    def normalize_tags(cls, value: Any) -> Any:
        if value is None or not isinstance(value, list):
            return value
        return list(dict.fromkeys(str(item).strip().lower() for item in value if str(item).strip()))


class TaskInDB(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime
    completed_at: datetime | None = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    status: TaskStatus
    priority: int
    due_date: date | None
    category: CategorySummary | None
    tags: list[str]
    created_at: datetime
    updated_at: datetime
    completed_at: datetime | None

    @computed_field
    @property
    def is_overdue(self) -> bool:
        return bool(self.due_date and self.due_date < date.today() and self.status != TaskStatus.COMPLETED)

    @computed_field
    @property
    def days_until_due(self) -> int | None:
        return (self.due_date - date.today()).days if self.due_date else None


class TaskPage(BaseModel):
    items: list[TaskResponse]
    total: int
    skip: int
    limit: int

