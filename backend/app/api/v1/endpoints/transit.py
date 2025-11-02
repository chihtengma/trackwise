"""
Transit endpoints.

This module handles real-time transit data from MTA.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_current_active_user
from app.models.user import User
from app.schemas.transit import RouteQuery, RouteResponse, TripUpdate
from app.services.transit import TransitService

router = APIRouter()


@router.get("/routes/{route_id}/updates", response_model=List[TripUpdate])
async def get_route_updates(
    route_id: str,
    current_user: User = Depends(get_current_active_user),
):
    """
    Get real-time trip updates for a specific route.

    Fetches live transit data for the specified MTA route.

    Args:
        route_id: Route identifier (e.g., "1", "A", "Q", "N")
        current_user: Current authenticated user

    Returns:
        List of trip updates with stop information

    Raises:
        HTTPException: If route not found or data unavailable

    Example Request:
        GET /api/v1/transit/routes/A/updates
        Authorization: Bearer <token>

    Example Response:
        [
            {
                "trip_id": "A-20241102-1",
                "route_id": "A",
                "start_time": "05:30:00",
                "start_date": "20241102",
                "stop_time_updates": [
                    {
                        "stop_id": "A01N",
                        "stop_name": "Inwood - 207 St",
                        "arrival_time": "2024-11-02T05:31:00Z",
                        "departure_time": "2024-11-02T05:32:00Z",
                        "delay": 0
                    }
                ]
            }
        ]
    """
    try:
        updates = await TransitService.get_trip_updates_for_route(route_id=route_id)
        return updates
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch route updates: {str(e)}",
        )


@router.post("/routes/query", response_model=RouteResponse)
async def query_routes(
    query: RouteQuery,
    current_user: User = Depends(get_current_active_user),
):
    """
    Query routes from origin to destination.

    This is a Phase 1 placeholder endpoint. Phase 2 will include
    AI-powered route optimization.

    Args:
        query: Route query parameters (origin, destination, preferences)
        current_user: Current authenticated user

    Returns:
        Route response with available route options

    Raises:
        HTTPException: If query parameters are invalid

    Example Request:
        POST /api/v1/transit/routes/query
        Authorization: Bearer <token>
        {
            "origin": "Times Sq-42 St",
            "destination": "Grand Central-42 St",
            "max_routes": 3,
            "prefer_less_crowded": false
        }

    Example Response:
        {
            "query": {
                "origin": "Times Sq-42 St",
                "destination": "Grand Central-42 St",
                "max_routes": 3,
                "prefer_less_crowded": false
            },
            "routes": [],
            "timestamp": "2024-11-02T12:00:00Z"
        }
    """
    try:
        response = await TransitService.query_routes(query=query)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to query routes: {str(e)}",
        )
