from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Settings:
    app_name: str = "Task Manager API"
    version: str = "1.0.0"
    cors_origins: tuple[str, ...] = ("http://localhost:5500", "http://127.0.0.1:5500")


settings = Settings()

