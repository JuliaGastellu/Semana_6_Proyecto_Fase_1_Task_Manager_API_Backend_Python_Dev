from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CategoryCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    name: str = Field(min_length=2, max_length=50, examples=["Trabajo"])
    color: str = Field(pattern=r"^#[0-9A-Fa-f]{6}$", examples=["#FF5733"])
    description: str | None = Field(default=None, max_length=300)


class CategorySummary(BaseModel):
    id: int
    name: str
    color: str


class CategoryResponse(CategorySummary):
    description: str | None
    created_at: datetime
    task_count: int


class CategoryInDB(CategoryCreate):
    id: int
    created_at: datetime

