# Task Manager API — Entrega de la semana 6

En esta entrega integré los conceptos de la fase 1 en una API de gestión de tareas. Organicé el proyecto por capas, mantuve los datos en memoria como pide la consigna y concentré las reglas de negocio en servicios para que los routers sean simples.

Implementé 13 rutas: health check; CRUD de tareas; listado, detalle, alta y baja de categorías; y listado, alta y baja de tags. El listado de tareas admite paginación y filtros por estado, prioridad, categoría y tag.

También incorporé validaciones estrictas con Pydantic, fechas futuras, normalización de tags, campos calculados para vencimientos, errores con `detail`, `error_code` y `status_code`, control de duplicados y conflictos, CORS, request ID, logging y medición de tiempos.

## Cómo lo ejecuto

```bash
uv sync
uv run fastapi dev app/main.py
```

La documentación interactiva queda en `http://127.0.0.1:8000/docs`. Como el almacenamiento es en memoria, los datos vuelven al estado inicial cuando reinicio el proceso.
