from fastapi import APIRouter, Depends, status

from app.dependencies import PaginationParams, TaskFilterParams, get_task_service
from app.schemas.task import TaskCreate, TaskPage, TaskResponse, TaskUpdate
from app.services.task_service import TaskService

router = APIRouter(prefix="/api/v1/tasks", tags=["tasks"])
NOT_FOUND = {404: {"description": "La tarea no existe"}}


@router.get("", response_model=TaskPage, summary="Listar tareas")
def list_tasks(page: PaginationParams = Depends(), filters: TaskFilterParams = Depends(), tasks: TaskService = Depends(get_task_service)) -> TaskPage:
    """Lista y combina filtros con una página que conserva el total."""
    matches = tasks.list_all(status=filters.status, priority=filters.priority, category_id=filters.category_id, tag=filters.tag)
    return TaskPage(items=[tasks.to_response(item) for item in matches[page.skip:page.skip + page.limit]], total=len(matches), skip=page.skip, limit=page.limit)


@router.get("/{task_id}", response_model=TaskResponse, summary="Obtener una tarea", responses=NOT_FOUND)
def get_task(task_id: int, tasks: TaskService = Depends(get_task_service)) -> TaskResponse:
    return tasks.to_response(tasks.get(task_id))


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED, summary="Crear una tarea", responses={404: {"description": "Categoría o tag inexistente"}})
def create_task(data: TaskCreate, tasks: TaskService = Depends(get_task_service)) -> TaskResponse:
    return tasks.to_response(tasks.create(data))


@router.put("/{task_id}", response_model=TaskResponse, summary="Actualizar una tarea", responses=NOT_FOUND)
def update_task(task_id: int, data: TaskUpdate, tasks: TaskService = Depends(get_task_service)) -> TaskResponse:
    return tasks.to_response(tasks.update(task_id, data))


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Borrar una tarea", responses=NOT_FOUND)
def delete_task(task_id: int, tasks: TaskService = Depends(get_task_service)) -> None:
    tasks.delete(task_id)

