from fastapi import APIRouter, Depends, status

from app.dependencies import get_category_service, get_task_service
from app.schemas.category import CategoryCreate, CategoryInDB, CategoryResponse
from app.services.category_service import CategoryService
from app.services.task_service import TaskService

router = APIRouter(prefix="/api/v1/categories", tags=["categories"])
ERRORS = {404: {"description": "No existe"}, 409: {"description": "Nombre repetido o categoría en uso"}}


def response(item: CategoryInDB, tasks: TaskService) -> CategoryResponse:
    return CategoryResponse(**item.model_dump(), task_count=tasks.count_by_category(item.id))


@router.get("", response_model=list[CategoryResponse], summary="Listar categorías")
def list_categories(categories: CategoryService = Depends(get_category_service), tasks: TaskService = Depends(get_task_service)) -> list[CategoryResponse]:
    return [response(item, tasks) for item in categories.list_all()]


@router.get("/{category_id}", response_model=CategoryResponse, summary="Obtener una categoría", responses=ERRORS)
def get_category(category_id: int, categories: CategoryService = Depends(get_category_service), tasks: TaskService = Depends(get_task_service)) -> CategoryResponse:
    return response(categories.get(category_id), tasks)


@router.post("", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED, summary="Crear una categoría", responses=ERRORS)
def create_category(data: CategoryCreate, categories: CategoryService = Depends(get_category_service), tasks: TaskService = Depends(get_task_service)) -> CategoryResponse:
    return response(categories.create(data), tasks)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Borrar una categoría", responses=ERRORS)
def delete_category(category_id: int, categories: CategoryService = Depends(get_category_service)) -> None:
    categories.delete(category_id)

