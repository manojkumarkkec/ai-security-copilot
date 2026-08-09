from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import AppException


async def app_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:

    if not isinstance(exc, AppException):
        raise exc

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.message,
            "path": request.url.path,
        },
    )


async def global_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:

    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "message": "Internal server error.",
            "path": request.url.path,
        },
    )