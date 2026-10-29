class TaskManagerError(Exception):
    error_code = "TASK_MANAGER_ERROR"

    def __init__(self, detail: str) -> None:
        self.detail = detail
        super().__init__(detail)


class NotFoundError(TaskManagerError):
    error_code = "NOT_FOUND"


class DuplicateError(TaskManagerError):
    error_code = "DUPLICATE"


class InUseError(TaskManagerError):
    error_code = "IN_USE"


STATUS_BY_ERROR = {"NOT_FOUND": 404, "DUPLICATE": 409, "IN_USE": 409}

