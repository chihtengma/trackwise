"""
Saved routes endpoints.

This module provides endpoints for managing user's saved transit routes.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_active_user
from app.core.database import get_async_db
from app.models.user import User
from app.schemas.saved_route import (
    SavedRouteCreate,
    SavedRouteListResponse,
    SavedRouteResponse,
    SavedRouteUpdate,
)
from app.services.saved_route import SavedRouteService

router = APIRouter()


@router.post(
    "/", response_model=SavedRouteResponse, status_code=status.HTTP_201_CREATED
)
async def create_saved_route(
    route_data: SavedRouteCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Create a new saved route.

    Save a frequently used transit route for quick access.

    Args:
        route_data: SavedRouteCreate schema with route information
        db: Database session
        current_user: Current authenticated user

    Returns:
        Created SavedRoute object

    Example Request:
        POST /api/v1/saved-routes
        {
            "name": "Home to Work",
            "origin": "Times Sq-42 St",
            "destination": "Grand Central-42 St",
            "is_favorite": true
        }
    """
    route = await SavedRouteService.create_route(
        db, route_data, user_id=current_user.id
    )
    return route


@router.get("/", response_model=SavedRouteListResponse)
async def list_saved_routes(
    skip: int = Query(0, ge=0, description="Number of routes to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum routes to return"),
    favorites_only: bool = Query(False, description="Only return favorite routes"),
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    List all saved routes for the current user.

    Returns a paginated list of saved routes.

    Args:
        skip: Number of routes to skip
        limit: Maximum number of routes to return
        favorites_only: If True, only return favorite routes
        db: Database session
        current_user: Current authenticated user

    Returns:
        SavedRouteListResponse with routes and counts

    Example Request:
        GET /api/v1/saved-routes?favorites_only=true
    """
    routes = await SavedRouteService.get_routes_by_user(
        db,
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        favorites_only=favorites_only,
    )
    favorites_count = await SavedRouteService.get_favorites_count(db, current_user.id)

    return SavedRouteListResponse(
        routes=routes,
        total=len(routes),
        favorites_count=favorites_count,
    )


@router.get("/{route_id}", response_model=SavedRouteResponse)
async def get_saved_route(
    route_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Get a specific saved route by ID.

    Retrieve details of a saved route.

    Args:
        route_id: The route's unique identifier
        db: Database session
        current_user: Current authenticated user

    Returns:
        SavedRoute object

    Raises:
        ResourceNotFoundError: If route not found (404)

    Example Request:
        GET /api/v1/saved-routes/1
    """
    route = await SavedRouteService.get_route_by_id(db, route_id, current_user.id)
    if not route:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Saved route not found",
        )
    return route


@router.put("/{route_id}", response_model=SavedRouteResponse)
async def update_saved_route(
    route_id: int,
    route_data: SavedRouteUpdate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Update a saved route.

    Modify details of an existing saved route.

    Args:
        route_id: The route's unique identifier
        route_data: SavedRouteUpdate schema with updated fields
        db: Database session
        current_user: Current authenticated user

    Returns:
        Updated SavedRoute object

    Raises:
        ResourceNotFoundError: If route not found (404)

    Example Request:
        PUT /api/v1/saved-routes/1
        {
            "name": "Updated Route Name",
            "is_favorite": true
        }
    """
    try:
        route = await SavedRouteService.update_route(
            db, route_id, route_data, user_id=current_user.id
        )
        return route
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.delete("/{route_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_saved_route(
    route_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Delete a saved route.

    Remove a saved route from the user's collection.

    Args:
        route_id: The route's unique identifier
        db: Database session
        current_user: Current authenticated user

    Returns:
        204 No Content on success

    Raises:
        ResourceNotFoundError: If route not found (404)

    Example Request:
        DELETE /api/v1/saved-routes/1
    """
    try:
        await SavedRouteService.delete_route(db, route_id, user_id=current_user.id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
