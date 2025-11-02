"""
Main FastAPI application entry point.

This module initializes the FastAPI application with all necessary
configurations, middlewares, and route handlers.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.api.v1 import api_router as api_v1_router
from app.core.exceptions import AppException
from app.core.exception_handlers import app_exception_handler
from app.core.cache import close_cache, get_cache
from app.core.scheduler import start_scheduler, stop_scheduler
from app.core.background_tasks import register_scheduled_jobs
from app.services.mta_client import close_mta_client
from app.services.weather_client import close_weather_client


# Define lifecycle event handlers
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.

    Use this to handle tasks that need to run when the app starts or stops,
    such as initializing database connections or cleaning up resources.
    """
    # --- Startup tasks ---
    print(f"🚀 Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"📝 Environment: {settings.ENVIRONMENT}")
    print(f"📚 API Docs: http://{settings.HOST}:{settings.PORT}/docs")
    print(f"🔗 API v1: http://{settings.HOST}:{settings.PORT}/api/v1")

    # Initialize cache connection
    await get_cache()

    # Start scheduler and register background tasks
    await start_scheduler()
    register_scheduled_jobs()

    yield  # <-- Application runs while inside this block

    # --- Shutdown tasks ---
    print(f"👋 Shutting down {settings.APP_NAME}")
    await stop_scheduler()  # Stop scheduler first
    await close_cache()  # Clean up Redis cache connection
    await close_mta_client()  # Clean up MTA client connection
    await close_weather_client()  # Clean up weather client connection


# Initialize the FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered transit assistant for NYC commuters",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# Configure CORS
# This allows the flutter frontend to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers (Authorization, Content-Type, etc.)
)

# Register custom exception handler for domain exceptions
app.add_exception_handler(AppException, app_exception_handler)

# Include API v1 router with /api/v1 prefix
app.include_router(
    api_v1_router,
    prefix="/api/v1",
)


@app.get("/", tags=["general"])
async def root():
    """
    Root endpoint - API information.

    Returns general information about the API including version,
    available endpoints, and documentation URLs.

    Returns:
        dict: API information and navigation

    Example:
        >>> # GET /
        >>> {
        ...     "message": "MTA Transit AI Assistant API",
        ...     "version": "0.1.0",
        ...     "status": "operational",
        ...     "docs": "/docs",
        ...     "api": "/api/v1"
        ... }
    """

    return {
        "message": f"{settings.APP_NAME} API",
        "version": settings.APP_VERSION,
        "status": "operational",
        "docs": "/docs",
        "api": "/api/v1",
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint.

    Returns the current status of the application and its dependencies.
    Useful for monitoring and load balancers.

    Returns:
        dict: Application health status

    Example:
        >>> # GET /health
        >>> {
        ...     "status": "healthy",
        ...     "environment": "development"
        ... }
    """
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
    }


# Exception handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    """
    Custom 404 error handler.

    Returns a JSON response for 404 Not Found errors.

    Args:
        request: The incoming request
        exc: The exception raised

    Returns:
        JSONResponse with error details
    """
    return JSONResponse(
        status_code=404,
        content={
            "detail": "Resource not found",
            "path": str(request.url),
        },
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """
    Custom 500 error handler.

    Returns a JSON response for 500 Internal Server errors.

    Args:
        request: The incoming request
        exc: The exception raised

    Returns:
        JSONResponse with error details
    """
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "message": "An unexpected error occurred. Please try again later.",
        },
    )


if __name__ == "__main__":
    import uvicorn

    # Run the application using uvicorn
    # This is useful for development, but use a process manager in production
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )
