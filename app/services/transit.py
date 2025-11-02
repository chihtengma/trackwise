"""
Transit service.

Business logic for transit data operations with caching.
"""

from typing import List
from datetime import datetime, timezone

from app.services.mta_client import get_mta_client
from app.schemas.transit import (
    TripUpdate,
    StopTimeUpdate,
    RouteQuery,
    RouteResponse,
    RouteOption,
)

# Import weather service for integration
try:
    from app.services.weather import WeatherService
except ImportError:
    WeatherService = None


class TransitService:
    """
    Service for transit operations.

    Handles route queries, trip updates, and transit data.
    """

    @staticmethod
    async def get_trip_updates_for_route(route_id: str) -> List[TripUpdate]:
        """
        Get real-time trip updates for a specific route.

        Args:
            route_id: Route identifier (e.g., "1", "A", "Q")

        Returns:
            List of TripUpdate objects

        Example:
            >>> updates = await TransitService.get_trip_updates_for_route("A")
            >>> print(f"Found {len(updates)} active trips")
        """
        client = get_mta_client()
        raw_updates = await client.get_trip_updates(route_id=route_id)

        # Convert to Pydantic models
        trip_updates = []
        for raw_update in raw_updates:
            # Convert stop time updates
            stop_updates = [
                StopTimeUpdate(
                    stop_id=stu["stop_id"],
                    arrival_time=stu.get("arrival_time"),
                    departure_time=stu.get("departure_time"),
                )
                for stu in raw_update["stop_time_updates"]
            ]

            trip_update = TripUpdate(
                trip_id=raw_update["trip_id"],
                route_id=raw_update["route_id"],
                start_time=raw_update.get("start_time"),
                start_date=raw_update.get("start_date"),
                stop_time_updates=stop_updates,
            )
            trip_updates.append(trip_update)

        return trip_updates

    @staticmethod
    async def query_routes(query: RouteQuery) -> RouteResponse:
        """
        Query routes from origin to destination.

        This is a simplified implementation for Phase 1.
        Phase 2 will include AI-powered route optimization.

        Args:
            query: Route query parameters

        Returns:
            RouteResponse with available routes

        Example:
            >>> query = RouteQuery(
            ...     origin="Times Sq-42 St",
            ...     destination="Grand Central-42 St",
            ...     max_routes=3
            ... )
            >>> response = await TransitService.query_routes(query)
        """
        # TODO: Implement actual route finding algorithm
        # For now, return a simple response structure

        routes: List[RouteOption] = []

        # This is a placeholder - Phase 2 will implement:
        # 1. Find all possible routes between origin and destination
        # 2. Calculate travel times using real-time data
        # 3. Rank routes by time, convenience, and crowding
        # 4. Apply AI recommendations

        # Fetch weather if requested
        weather = None
        if query.include_weather and query.weather_location:
            try:
                if WeatherService:
                    weather = await WeatherService.get_current_weather(
                        query.weather_location
                    )
            except Exception:
                # If weather fetch fails, return None (don't fail the entire request)
                weather = None

        return RouteResponse(
            query=query,
            routes=routes,
            timestamp=datetime.now(timezone.utc),
            weather=weather,
        )
