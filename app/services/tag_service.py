from datetime import datetime, timezone

from app.exceptions import DuplicateError, InUseError, NotFoundError
from app.schemas.tag import TagCreate, TagInDB


class TagService:
    def __init__(self) -> None:
        self._items: dict[int, TagInDB] = {}
        self._next_id = 1
        self._usage_checker = lambda _name: 0

    def set_usage_checker(self, checker: object) -> None:
        self._usage_checker = checker  # type: ignore[assignment]

    def list_all(self) -> list[TagInDB]:
        return [item.model_copy(deep=True) for item in self._items.values()]

    def get_by_name(self, name: str) -> TagInDB:
        wanted = name.casefold()
        for item in self._items.values():
            if item.name.casefold() == wanted:
                return item.model_copy(deep=True)
        raise NotFoundError(f"El tag {name} no existe")

    def get(self, tag_id: int) -> TagInDB:
        if tag_id not in self._items:
            raise NotFoundError(f"El tag {tag_id} no existe")
        return self._items[tag_id].model_copy(deep=True)

    def create(self, data: TagCreate) -> TagInDB:
        if any(item.name == data.name for item in self._items.values()):
            raise DuplicateError(f"Ya existe un tag con el nombre '{data.name}'")
        item = TagInDB(**data.model_dump(), id=self._next_id, created_at=datetime.now(timezone.utc))
        self._items[item.id] = item
        self._next_id += 1
        return item.model_copy(deep=True)

    def delete(self, tag_id: int) -> None:
        item = self.get(tag_id)
        count = self._usage_checker(item.name)
        if count:
            raise InUseError(f"El tag {item.name} tiene {count} tarea(s) asignada(s): no se puede borrar")
        del self._items[tag_id]

