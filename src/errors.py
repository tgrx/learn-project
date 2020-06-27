from typing import Optional


class AppError(RuntimeError):
    pass


class NotFound(AppError):
    def __init__(self, *args, extra: Optional[str] = None):
        super().__init__(*args)
        self.extra = extra


class MethodNotAllowed(AppError):
    ...


class UnknownPath(AppError):
    pass
