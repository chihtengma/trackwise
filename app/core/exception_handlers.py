"""
Global exception handlers for FastAPI.

Converts domain exceptions to appropriate HTTP responses.
"""

from typing import Union

from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import AppException


async def app_exception_handler(
    request: Request, exc: Union[AppException, Exception]
) -> JSONResponse:
    """
    Generic handler for application exceptions.

    Uses the status_code attribute from the exception class.
    This provides a good default while allowing override if needed.

    Args:
        request: The incoming request
        exc: The application exception

    Returns:
        JSONResponse with error details

    Example:
        The response will look like:
        {
            "detail": "User not found",
            "error_type": "ResourceNotFoundError",
            "user_id": 123
        }
    """
    # Handle AppException subclasses
    if isinstance(exc, AppException):
        return JSONResponse(
            status_code=exc.status_code,  # Use status_code from exception class
            content={
                "detail": exc.message,
                "error_type": type(exc).__name__,
                **exc.details,  # Merge additional details
            },
        )
    # Fallback for generic exceptions
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc), "error_type": "Exception"},
    )
