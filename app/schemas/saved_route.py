"""
Saved route schemas for request/response validation.

This module defines Pydantic models for saved route data validation,
serialization, and API documentation.
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


# ==================== Base Schemas ====================


class SavedRouteBase(BaseModel):
    """
    Base schema for saved routes with common fields.
    """

    name: str = Field(
        ..., min_length=1, max_length=255, description="Name for this saved route"
    )
    origin: str = Field(
        ..., min_length=1, max_length=255, description="Origin stop or location"
    )
    destination: str = Field(
        ..., min_length=1, max_length=255, description="Destination stop or location"
    )
    route_types: Optional[str] = Field(
        None,
        max_length=100,
        description="Preferred route types (comma-separated: subway,bus)",
    )
    notes: Optional[str] = Field(None, description="Optional notes about the route")


# ==================== Request Schemas ====================


class SavedRouteCreate(SavedRouteBase):
    """
    Schema for creating a new saved route.
    """

    is_favorite: bool = Field(
        default=False, description="Whether this is a favorite route"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Home to Work",
                "origin": "Times Sq-42 St",
                "destination": "Grand Central-42 St",
                "route_types": "subway",
                "notes": "My morning commute",
                "is_favorite": True,
            }
        }
    }


class SavedRouteUpdate(BaseModel):
    """
    Schema for updating a saved route.

    All fields are optional since users may update only specific fields.
    """

    name: Optional[str] = Field(
        None, min_length=1, max_length=255, description="Updated route name"
    )
    origin: Optional[str] = Field(
        None, min_length=1, max_length=255, description="Updated origin"
    )
    destination: Optional[str] = Field(
        None, min_length=1, max_length=255, description="Updated destination"
    )
    route_types: Optional[str] = Field(
        None,
        max_length=100,
        description="Updated preferred route types",
    )
    notes: Optional[str] = Field(None, description="Updated notes")
    is_favorite: Optional[bool] = Field(None, description="Updated favorite status")
    is_active: Optional[bool] = Field(None, description="Updated active status")

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Home to Work (Updated)",
                "is_favorite": True,
            }
        }
    }


# ==================== Response Schemas ====================


class SavedRouteResponse(SavedRouteBase):
    """
    Schema for saved route responses.
    """

    id: int = Field(..., description="Route ID")
    user_id: int = Field(..., description="User ID who owns this route")
    is_favorite: bool = Field(..., description="Whether this is a favorite route")
    is_active: bool = Field(..., description="Whether the route is active")
    created_at: datetime = Field(..., description="When the route was created")
    updated_at: datetime = Field(..., description="When the route was last updated")

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "user_id": 1,
                "name": "Home to Work",
                "origin": "Times Sq-42 St",
                "destination": "Grand Central-42 St",
                "route_types": "subway",
                "notes": "My morning commute",
                "is_favorite": True,
                "is_active": True,
                "created_at": "2025-11-02T10:00:00Z",
                "updated_at": "2025-11-02T10:00:00Z",
            }
        },
    }


class SavedRouteListResponse(BaseModel):
    """
    Schema for listing saved routes.
    """

    routes: List[SavedRouteResponse] = Field(..., description="List of saved routes")
    total: int = Field(..., description="Total number of routes")
    favorites_count: int = Field(..., description="Number of favorite routes")

    model_config = {
        "json_schema_extra": {
            "example": {
                "routes": [],
                "total": 0,
                "favorites_count": 0,
            }
        }
    }


# ==================== User Preferences Schemas ====================


class UserPreferences(BaseModel):
    """
    Schema for user preferences.
    """

    theme: Optional[str] = Field(None, description="UI theme preference")
    default_units: Optional[str] = Field(
        "metric", description="Default temperature units (metric/imperial)"
    )
    notification_enabled: Optional[bool] = Field(
        True, description="Enable notifications"
    )
    favorite_stops: Optional[List[str]] = Field(
        None, description="List of favorite stop IDs"
    )
    preferred_routes: Optional[List[str]] = Field(
        None, description="List of preferred route IDs"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "theme": "dark",
                "default_units": "imperial",
                "notification_enabled": True,
                "favorite_stops": ["127N", "A28S"],
                "preferred_routes": ["A", "1", "2"],
            }
        }
    }
