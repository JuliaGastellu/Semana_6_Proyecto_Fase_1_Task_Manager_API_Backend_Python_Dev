import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.exceptions import STATUS_BY_ERROR, TaskManagerError
from app.middleware.request_logging import RequestLoggingMiddleware
from app.routers import categories, tags, tasks

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s %(message)s")

tags_metadata = [
    {"name": "health", "description": "Estado del servicio."},
    {"name": "tasks", "description": "CRUD, filtros y paginación de tareas."},
    {"name": "categories", "description": "Catálogo de categorías."},
    {"name": "tags", "description": "Catálogo de etiquetas."},
]

app = FastAPI(title=settings.app_name, version=settings.version, openapi_tags=tags_metadata)
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(CORSMiddleware, allow_origins=list(settings.cors_origins), allow_credentials=True, allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"], allow_headers=["Content-Type", "X-Request-ID"], expose_headers=["X-Request-ID", "X-Process-Time"])


@app.exception_handler(TaskManagerError)
async def task_manager_error_handler(request: Request, exc: TaskManagerError) -> JSONResponse:
    code = STATUS_BY_ERROR[exc.error_code]
    return JSONResponse(status_code=code, content={"detail": exc.detail, "error_code": exc.error_code, "status_code": code}, headers={"X-Request-ID": getattr(request.state, "request_id", "unknown")})


@app.get("/", tags=["health"], summary="Comprobar el estado")
def health() -> dict[str, str]:
    return {"status": "healthy", "service": "task-manager-api", "version": settings.version}


app.include_router(tasks.router)
app.include_router(categories.router)
app.include_router(tags.router)

