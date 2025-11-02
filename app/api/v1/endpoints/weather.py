"""
Weather endpoints.

This module handles weather data from OpenWeatherMap.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query

from app.api.dependencies import get_current_active_user
from app.models.user import User
from app.schemas.weather import WeatherQuery, WeatherCurrentResponse
from app.services.weather import WeatherService

router = APIRouter()


@router.get("/current", response_model=WeatherCurrentResponse)
async def get_current_weather(
    location: str = Query(
        ...,
        description=(
            "Location name or coordinates (e.g., 'New York' or '40.7128,-74.0060')"
        ),
    ),
    units: str = Query(
        default="metric",
        description="Temperature units: metric (C), imperial (F), or kelvin",
    ),
    current_user: User = Depends(get_current_active_user),
):
    """
    Get current weather for a location.

    Fetches current weather data from OpenWeatherMap.

    Args:
        location: Location name or coordinates
        units: Temperature units (metric=°C, imperial=°F, kelvin=K)
        current_user: Current authenticated user

    Returns:
        Current weather information

    Raises:
        HTTPException: If location not found or API error

    Example Request:
        GET /api/v1/weather/current?location=New+York&units=metric
        Authorization: Bearer <token>

    Example Response:
        {
            "location": "New York",
            "temp_celsius": 15.0,
            "temp_fahrenheit": 59.0,
            "feels_like_celsius": 14.7,
            "condition": "Clear",
            "description": "clear sky",
            "humidity": 65,
            "wind_speed": 4.5,
            "visibility_km": 10.0
        }
    """
    try:
        weather = await WeatherService.get_current_weather(location, units)
        return weather
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch weather: {str(e)}",
        )


@router.post("/query", response_model=WeatherCurrentResponse)
async def query_weather(
    query: WeatherQuery,
    units: str = Query(
        default="metric",
        description="Temperature units: metric, imperial, or kelvin",
    ),
    current_user: User = Depends(get_current_active_user),
):
    """
    Query weather for a location.

    Alternative POST endpoint for weather queries.

    Args:
        query: Weather query parameters
        units: Temperature units (metric=°C, imperial=°F, kelvin=K)
        current_user: Current authenticated user

    Returns:
        Current weather information

    Raises:
        HTTPException: If location not found or API error

    Example Request:
        POST /api/v1/weather/query?units=metric
        Authorization: Bearer <token>
        {
            "location": "New York"
        }
    """
    try:
        weather = await WeatherService.get_current_weather(query.location, units)
        return weather
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch weather: {str(e)}",
        )
