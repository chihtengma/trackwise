"""
Transit data schemas.

Pydantic models for MTA GTFS-Realtime data structures.
"""

from datetime import datetime
from typing import List, Optional
from enum import Enum

from pydantic import BaseModel, Field

# Import weather schema for integration
try:
    from app.schemas.weather import WeatherCurrentResponse
except ImportError:
    # Handle circular import if it occurs
    WeatherCurrentResponse = None


class RouteType(Enum):
    """Transit route types"""

    SUBWAY = "subway"
    BUS = "bus"
    RAIL = "rail"


class TripDirection(Enum):
    """Trip direction"""

    NORTH = "north"
    SOUTH = "south"
    EAST = "east"
    WEST = "west"


class StopTimeUpdate(BaseModel):
    """
    Real-time update for a stop on a trip.

    Represents when a train/bus will arrive at a specific stop.
    """

    stop_id: str = Field(..., description="Stop identifier")
    stop_name: Optional[str] = Field(
        None,
        description="Human-readable stop name",
    )
    arrival_time: Optional[datetime] = Field(
        None,
        description="Expected arrival time",
    )
    departure_time: Optional[datetime] = Field(
        None,
        description="Expected departure time",
    )
    delay: Optional[int] = Field(
        None,
        description="Delay in seconds (positive = late)",
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "stop_id": "127N",
                "stop_name": "Times Square - 42nd Street",
                "arrival_time": "2025-11-01T15:30:00Z",
                "departure_time": "2025-11-01T15:31:00Z",
                "delay": 120,
            }
        }
    }


class TripUpdate(BaseModel):
    """
    Real-time trip update from GTFS-Realtime feed.
    """

    trip_id: str = Field(..., description="Trip identifier")
    route_id: str = Field(..., description="Route identifier")
    start_time: Optional[str] = Field(None, description="Trip start time")
    start_date: Optional[str] = Field(None, description="Trip start date")
    stop_time_updates: List[StopTimeUpdate] = Field(
        default_factory=list, description="Stop time updates"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "trip_id": "A-20171201-1",
                "route_id": "A",
                "start_time": "05:30:00",
                "start_date": "20251101",
                "stop_time_updates": [],
            }
        }
    }


class RouteInfo(BaseModel):
    """
    Information about a transit route.
    """

    route_id: str = Field(..., description="Route identifier")
    route_name: str = Field(..., description="Route name/number")
    route_type: RouteType = Field(..., description="Type of route")
    route_color: Optional[str] = Field(
        None,
        description="Hex color code for route (e.g. #FF0000)",
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "route_id": "1",
                "route_name": "1 Line Subway",
                "route_type": "subway",
                "route_color": "#EE352E",
            }
        }
    }


class StopInfo(BaseModel):
    """
    Information about a transit stop/station.
    """

    stop_id: str = Field(..., description="Stop identifier")
    stop_name: str = Field(..., description="Stop name")
    stop_lat: Optional[float] = Field(
        None,
        description="Latitude of stop location",
    )
    stop_lon: Optional[float] = Field(
        None,
        description="Longitude of stop location",
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "stop_id": "127N",
                "stop_name": "Times Square - 42nd Street",
                "stop_lat": 40.758895,
                "stop_lon": -73.985130,
            }
        }
    }


class RouteQuery(BaseModel):
    """
    Request schema for route queries.
    """

    origin: str = Field(
        ...,
        description="Origin stop ID or name",
    )
    destination: str = Field(
        ...,
        description="Destination stop ID or name",
    )
    departure_time: Optional[datetime] = Field(
        None,
        description="Desired departure time (defaults to now)",
    )
    max_routes: int = Field(
        default=3,
        ge=1,
        le=10,
        description="Maximum number of routes to return (1-10)",
    )
    prefer_less_crowded: bool = Field(
        default=False,
        description="Prefer less crowded routes (True) or fastest routes (False)",
    )
    include_weather: bool = Field(
        default=False,
        description=(
            "Include weather information in response (requires weather_location)"
        ),
    )
    weather_location: Optional[str] = Field(
        None,
        description="Location for weather data (e.g., 'New York')",
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "origin": "Times Sq-42 St",
                "destination": "Grand Central-42 St",
                "departure_time": "2025-10-31T14:30:00Z",
                "max_routes": 3,
                "prefer_less_crowded": False,
                "include_weather": True,
                "weather_location": "New York",
            }
        }
    }


class RouteSegment(BaseModel):
    """
    A segment of a route (e.g., take the 1 train from A to B).
    """

    route_id: str = Field(..., description="Route identifier")
    route_name: str = Field(..., description="Route name/number")
    origin_stop: StopInfo = Field(..., description="Origin stop")
    destination_stop: StopInfo = Field(..., description="Destination stop")
    departure_time: Optional[datetime] = Field(None, description="Departure time")
    arrival_time: Optional[datetime] = Field(None, description="Arrival time")
    duration_minutes: Optional[int] = Field(
        None, description="Segment duration in minutes"
    )
    num_stops: int = Field(..., description="Number of stops on this segment")


class RouteOption(BaseModel):
    """
    A complete route from origin to destination.

    May include multiple segments (transfers, walking, etc.)
    """

    segments: List[RouteSegment] = Field(..., description="Route segments")
    total_duration_minutes: int = Field(..., description="Total travel time in minutes")
    num_transfers: int = Field(..., description="Number of transfers required")
    departure_time: datetime = Field(..., description="Total route departure time")
    arrival_time: datetime = Field(..., description="Total route arrival time")
    estimated_crowding: Optional[str] = Field(
        None,
        description="Estimated crowding level (low, medium, high) (Phase 2 feature)",
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "segments": [],
                "total_duration_minutes": 15,
                "num_transfers": 0,
                "departure_time": "2025-10-31T14:30:00Z",
                "arrival_time": "2025-10-31T14:45:00Z",
                "estimated_crowding": "medium",
            }
        }
    }


class RouteResponse(BaseModel):
    """
    Response schema for route queries.
    """

    query: RouteQuery = Field(..., description="Original query parameters")
    routes: List[RouteOption] = Field(..., description="Available route options")
    timestamp: datetime = Field(..., description="Response generation timestamp")
    weather: Optional["WeatherCurrentResponse"] = Field(
        None,
        description="Current weather at destination (if location provided)",
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "query": {
                    "origin": "Times Sq-42 St",
                    "destination": "Grand Central-42 St",
                    "max_routes": 3,
                },
                "routes": [],
                "timestamp": "2025-10-31T14:30:00Z",
                "weather": None,
            }
        }
    }
