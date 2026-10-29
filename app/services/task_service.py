from datetime import datetime, timezone

from app.exceptions import NotFoundError
from app.schemas.category import CategorySummary
from app.schemas.task import TaskCreate, TaskInDB, TaskResponse, TaskStatus, TaskUpdate
from app.services.category_service import CategoryService
from app.services.tag_service import TagService


class TaskService:
    def __init__(self, categories: CategoryService, tags: TagService) -> None:
        self._categories = categories
        self._tags = tags
        self._items: dict[int, TaskInDB] = {}
        self._next_id = 1

    def _validate_references(self, category_id: int | None, tags: list[str]) -> None:
        if category_id is not None:
            self._categories.get(category_id)
        for tag in tags:
            self._tags.get_by_name(tag)

    def create(self, data: TaskCreate) -> TaskInDB:
        self._validate_references(data.category_id, data.tags)
        now = datetime.now(timezone.utc)
        completed_at = now if data.status == TaskStatus.COMPLETED else None
        item = TaskInDB(**data.model_dump(), id=self._next_id, created_at=now, updated_at=now, completed_at=completed_at)
        self._items[item.id] = item
        self._next_id += 1
        return item.model_copy(deep=True)

    def get(self, task_id: int) -> TaskInDB:
        if task_id not in self._items:
            raise NotFoundError(f"La tarea {task_id} no existe")
        return self._items[task_id].model_copy(deep=True)

    def list_all(self, *, status: TaskStatus | None = None, priority: int | None = None, category_id: int | None = None, tag: str | None = None) -> list[TaskInDB]:
        return [item.model_copy(deep=True) for item in self._items.values() if (status is None or item.status == status) and (priority is None or item.priority == priority) and (category_id is None or item.category_id == category_id) and (tag is None or tag.casefold() in item.tags)]

    def update(self, task_id: int, data: TaskUpdate) -> TaskInDB:
        current = self.get(task_id)
        changes = data.model_dump(exclude_unset=True)
        category_id = changes.get("category_id", current.category_id)
        tags = changes.get("tags", current.tags)
        self._validate_references(category_id, tags)
        status = changes.get("status", current.status)
        changes["completed_at"] = datetime.now(timezone.utc) if status == TaskStatus.COMPLETED else None
        changes["updated_at"] = datetime.now(timezone.utc)
        updated = TaskInDB.model_validate({**current.model_dump(), **changes})
        self._items[task_id] = updated
        return updated.model_copy(deep=True)

    def delete(self, task_id: int) -> None:
        self.get(task_id)
        del self._items[task_id]

    def count_by_category(self, category_id: int) -> int:
        return sum(item.category_id == category_id for item in self._items.values())

    def count_by_tag(self, name: str) -> int:
        return sum(name.casefold() in item.tags for item in self._items.values())

    def to_response(self, item: TaskInDB) -> TaskResponse:
        category = None
        if item.category_id is not None:
            stored = self._categories.get(item.category_id)
            category = CategorySummary(id=stored.id, name=stored.name, color=stored.color)
        return TaskResponse(**item.model_dump(exclude={"category_id"}), category=category)

