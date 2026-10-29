from fastapi import Depends, Query

from app.schemas.task import TaskStatus
from app.services.category_service import CategoryService
from app.services.tag_service import TagService
from app.services.task_service import TaskService

category_service = CategoryService()
tag_service = TagService()
task_service = TaskService(category_service, tag_service)
category_service.set_usage_checker(task_service.count_by_category)
tag_service.set_usage_checker(task_service.count_by_tag)


def get_category_service() -> CategoryService:
    return category_service


def get_tag_service() -> TagService:
    return tag_service


def get_task_service() -> TaskService:
    return task_service


class PaginationParams:
    def __init__(self, skip: int = Query(0, ge=0), limit: int = Query(20, ge=1, le=100)) -> None:
        self.skip = skip
        self.limit = limit


class TaskFilterParams:
    def __init__(self, status: TaskStatus | None = None, priority: int | None = Query(None, ge=1, le=5), category_id: int | None = Query(None, gt=0), tag: str | None = None) -> None:
        self.status = status
        self.priority = priority
        self.category_id = category_id
        self.tag = tag.lower() if tag else None


TaskServiceDep = Depends(get_task_service)

