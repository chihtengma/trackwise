"""
Custom middleware for the application.

This module defines middleware for rate limiting and other production features.
"""

from typing import Callable

from fastapi import Request, Response
from slowapi import Limiter, _rate_limit_exceeded_handler  # type: ignore
from slowapi.errors import RateLimitExceeded  # type: ignore
from slowapi.util import get_remote_address  # type: ignore

from app.core.config import settings


def get_rate_limiter() -> Limiter:
    """
    Get rate limiter instance.

    Returns:
        Limiter instance configured with Redis if available, memory otherwise
    """
    key_func: Callable[[Request], str] = get_remote_address

    # Try to use Redis for distributed rate limiting
    try:
        # Redis-based limiter for production
        limiter = Limiter(
            key_func=key_func,
            storage_uri=settings.REDIS_URL,
            default_limits=[f"{settings.RATE_LIMIT_PER_MINUTE}/minute"],
        )
    except Exception:
        # Fall back to in-memory limiter
        limiter = Limiter(
            key_func=key_func,
            default_limits=[f"{settings.RATE_LIMIT_PER_MINUTE}/minute"],
        )

    return limiter


# Create global limiter instance
rate_limiter = get_rate_limiter()


def get_rate_limit_exceeded_handler(app):
    """
    Configure rate limit exceeded handler.

    Args:
        app: FastAPI application instance

    Returns:
        Handler function for rate limit exceptions
    """
    app.state.limiter = rate_limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


async def add_security_headers(request: Request, call_next: Callable) -> Response:
    """
    Add security headers to all responses.

    Args:
        request: Incoming request
        call_next: Next middleware/handler

    Returns:
        Response with security headers
    """
    response = await call_next(request)

    # Security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000"

    return response
