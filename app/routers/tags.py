from fastapi import APIRouter, Depends, status

from app.dependencies import get_tag_service, get_task_service
from app.schemas.tag import TagCreate, TagInDB, TagResponse
from app.services.tag_service import TagService
from app.services.task_service import TaskService

router = APIRouter(prefix="/api/v1/tags", tags=["tags"])
ERRORS = {404: {"description": "No existe"}, 409: {"description": "Nombre repetido o tag en uso"}}


def response(item: TagInDB, tasks: TaskService) -> TagResponse:
    return TagResponse(**item.model_dump(), task_count=tasks.count_by_tag(item.name))


@router.get("", response_model=list[TagResponse], summary="Listar tags")
def list_tags(tags: TagService = Depends(get_tag_service), tasks: TaskService = Depends(get_task_service)) -> list[TagResponse]:
    return [response(item, tasks) for item in tags.list_all()]


@router.post("", response_model=TagResponse, status_code=status.HTTP_201_CREATED, summary="Crear un tag", responses=ERRORS)
def create_tag(data: TagCreate, tags: TagService = Depends(get_tag_service), tasks: TaskService = Depends(get_task_service)) -> TagResponse:
    return response(tags.create(data), tasks)


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Borrar un tag", responses=ERRORS)
def delete_tag(tag_id: int, tags: TagService = Depends(get_tag_service)) -> None:
    tags.delete(tag_id)

