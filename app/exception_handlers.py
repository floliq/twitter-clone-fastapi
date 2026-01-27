from typing import Any

from fastapi import HTTPException, Request, status
from starlette.responses import JSONResponse

from app.schemas.response import ResponseError


class CustomHTTPException(HTTPException):
    def __init__(
        self,
        status_code: int,
        error_type: str,
        error_message: str,
        detail: Any = None,
        headers: dict[str, str] | None = None,
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)
        self.error_type = error_type
        self.error_message = error_message


def custom_http_exception_handler(request: Request, exc: CustomHTTPException):
    error_response = ResponseError(result=False, error_type=exc.error_type, error_message=exc.error_message)

    return JSONResponse(status_code=exc.status_code, content=error_response.model_dump(), headers=exc.headers)


def global_exception_handler(request: Request, exc: Exception):
    error_response = ResponseError(result=False, error_type="internal_error", error_message=str(exc))

    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=error_response.model_dump())
