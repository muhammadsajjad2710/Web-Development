"""Reusable exception types and FastAPI handlers."""

from typing import Any, Dict, Optional

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


class AppException(Exception):
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        code: str = "app_error",
        details: Optional[Dict[str, Any]] = None,
    ):
        self.message = message
        self.status_code = status_code
        self.code = code
        self.details = details or {}
        super().__init__(message)


class NotFoundError(AppException):
    def __init__(self, message: str = "Resource not found", details: Optional[Dict] = None):
        super().__init__(message, status.HTTP_404_NOT_FOUND, "not_found", details)


class UnauthorizedError(AppException):
    def __init__(self, message: str = "Not authenticated", details: Optional[Dict] = None):
        super().__init__(message, status.HTTP_401_UNAUTHORIZED, "unauthorized", details)


class ForbiddenError(AppException):
    def __init__(self, message: str = "Permission denied", details: Optional[Dict] = None):
        super().__init__(message, status.HTTP_403_FORBIDDEN, "forbidden", details)


class ConflictError(AppException):
    def __init__(self, message: str = "Conflict", details: Optional[Dict] = None):
        super().__init__(message, status.HTTP_409_CONFLICT, "conflict", details)


class ValidationAppError(AppException):
    def __init__(self, message: str = "Validation error", details: Optional[Dict] = None):
        super().__init__(message, status.HTTP_422_UNPROCESSABLE_ENTITY, "validation_error", details)


def _error_body(code: str, message: str, details: Any = None) -> Dict[str, Any]:
    body: Dict[str, Any] = {"success": False, "error": {"code": code, "message": message}}
    if details is not None:
        body["error"]["details"] = details
    return body


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppException)
    async def app_exception_handler(_: Request, exc: AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content=_error_body(exc.code, exc.message, exc.details or None),
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(_: Request, exc: StarletteHTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content=_error_body("http_error", str(exc.detail)),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(_: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=_error_body("validation_error", "Request validation failed", exc.errors()),
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(_: Request, exc: Exception):
        # Avoid leaking internals in production responses
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=_error_body("internal_error", "An unexpected error occurred"),
        )
