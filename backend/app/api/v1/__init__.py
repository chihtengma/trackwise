"""
API v1 router configuration.

This module combines all v1 API endpoints and applies the /api/v1 prefix.
"""

from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    cache,
    saved_routes,
    scheduler,
    transit,
    users,
    weather,
)

# Crate the main v1 router
api_router = APIRouter()

api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["authentication"],
)

api_router.include_router(
    cache.router,
    prefix="/cache",
    tags=["cache"],
)

api_router.include_router(
    scheduler.router,
    prefix="/scheduler",
    tags=["scheduler"],
)

api_router.include_router(
    saved_routes.router,
    prefix="/saved-routes",
    tags=["saved-routes"],
)

api_router.include_router(
    transit.router,
    prefix="/transit",
    tags=["transit"],
)

api_router.include_router(
    users.router,
    prefix="/users",
    tags=["users"],
)

api_router.include_router(
    weather.router,
    prefix="/weather",
    tags=["weather"],
)
