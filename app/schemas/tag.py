from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TagCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    name: str = Field(min_length=2, max_length=30, pattern=r"^[A-Za-z0-9-]+$", examples=["urgent"])

    @field_validator("name")
    @classmethod
    def lowercase(cls, value: str) -> str:
        return value.lower()


class TagInDB(TagCreate):
    id: int
    created_at: datetime


class TagResponse(TagInDB):
    task_count: int

