"""
Pydantic schemas package.

This package contains all the Pydantic models for request/response validation.
Import all schemas here for easier access.
"""

from app.schemas.user import (
    UserBase,
    UserCreate,
    UserUpdate,
    UserInDB,
    UserResponse,
    Token,
    TokenData,
)
from app.schemas.saved_route import (
    SavedRouteBase,
    SavedRouteCreate,
    SavedRouteUpdate,
    SavedRouteResponse,
    SavedRouteListResponse,
    UserPreferences,
)

__all__ = [
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserInDB",
    "UserResponse",
    "Token",
    "TokenData",
    "SavedRouteBase",
    "SavedRouteCreate",
    "SavedRouteUpdate",
    "SavedRouteResponse",
    "SavedRouteListResponse",
    "UserPreferences",
]
