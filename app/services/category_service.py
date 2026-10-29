from datetime import datetime, timezone

from app.exceptions import DuplicateError, InUseError, NotFoundError
from app.schemas.category import CategoryCreate, CategoryInDB


class CategoryService:
    def __init__(self) -> None:
        self._items: dict[int, CategoryInDB] = {}
        self._next_id = 1
        self._usage_checker = lambda _category_id: 0

    def set_usage_checker(self, checker: object) -> None:
        self._usage_checker = checker  # type: ignore[assignment]

    def list_all(self) -> list[CategoryInDB]:
        return [item.model_copy(deep=True) for item in self._items.values()]

    def get(self, category_id: int) -> CategoryInDB:
        if category_id not in self._items:
            raise NotFoundError(f"La categoría {category_id} no existe")
        return self._items[category_id].model_copy(deep=True)

    def create(self, data: CategoryCreate) -> CategoryInDB:
        if any(item.name.casefold() == data.name.casefold() for item in self._items.values()):
            raise DuplicateError(f"Ya existe una categoría con el nombre '{data.name}'")
        item = CategoryInDB(**data.model_dump(), id=self._next_id, created_at=datetime.now(timezone.utc))
        self._items[item.id] = item
        self._next_id += 1
        return item.model_copy(deep=True)

    def delete(self, category_id: int) -> None:
        self.get(category_id)
        count = self._usage_checker(category_id)
        if count:
            raise InUseError(f"La categoría {category_id} tiene {count} tarea(s) asignada(s): no se puede borrar")
        del self._items[category_id]

