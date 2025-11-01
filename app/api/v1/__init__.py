"""
API v1 router configuration.

This module combines all v1 API endpoints and applies the /api/v1 prefix.
"""

from fastapi import APIRouter

from app.api.v1.endpoints import auth, users

# Crate the main v1 router
api_router = APIRouter()

api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["authentication"],
)

api_router.include_router(
    users.router,
    prefix="/users",
    tags=["users"],
)
