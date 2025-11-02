"""
MTA API Client.

Service for fetching real-time transit data from MTA GTFS-Realtime feeds.
"""

from google import protobuf
import httpx
from typing import Optional, Dict, List
from datetime import datetime

from google.transit import gtfs_realtime_pb2

from app.core.config import settings
from app.core.exceptions import ValidationError


class MTAClient:
    """
    Client for MTA GTFS-Realtime API.

    Handles fetching and parsing real-time transit data.
    """

    # Available feed IDs and their routes
    FEED_MAPPING = {
        "gtfs-ace": ["A", "C", "E", "H", "FS"],
        "gtfs-bdfm": ["B", "D", "F", "M"],
        "gtfs-g": ["G"],
        "gtfs-jz": ["J", "Z"],
        "gtfs-nqrw": ["N", "Q", "R", "W"],
        "gtfs-l": ["L"],
        "gtfs": ["1", "2", "3", "4", "5", "6", "7", "GS", "SI"],
    }

    def __init__(self):
        """Initialize the MTA client."""
        self.base_url = settings.MTA_SUBWAY_GTFS_RT_BASE_URL
        self.api_key = settings.MTA_API_KEY
        self.client = httpx.AsyncClient(timeout=30.0)

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()

    def get_feed_id_for_route(self, route_id: str) -> Optional[str]:
        """
        Get the feed ID for a given route.

        Args:
            route_id: MTA route ID (e.g., "A", "1", "B", etc.)

        Returns:
            Feed ID or None if route not found.

        Example:
            >>> client = MTAClient()
            >>> client.get_feed_id_for_route("A")
            "gtfs-ace"
        """
        route_id = (
            route_id.upper()
        )  # Convert to uppercase for case-insensitive matching
        for feed_id, routes in self.FEED_MAPPING.items():
            if route_id in routes:
                return feed_id
        return None

    async def fetch_feed(self, feed_id: str) -> gtfs_realtime_pb2.FeedMessage:
        """
        Fetch a GTFS-Realtime feed.

        Args:
            feed_id: Feed identifier (e.g., "gtfs-ace", "gtfs-bdfm", etc.)

        Returns:
            Parsed FeedMessage protobuf object.

        Raises:
            ValidationError: If feed cannot be fetched or parsed.

        Example:
            >>> client = MTAClient()
            >>> feed = await client.fetch_feed("gtfs-ace")
            >>> print(f"Feed has {len(feed.entity)} entities")
        """

        url = f"{self.base_url}%2F{feed_id}"  # Construct full URL with %2F

        # Prepare headers with API key if available
        headers = {}
        if self.api_key:
            headers["x-api-key"] = self.api_key

        try:
            response = await self.client.get(url, headers=headers)  # Fetch the feed
            response.raise_for_status()  # Status check (404, 500, etc.)
        except httpx.HTTPError as err:
            raise ValidationError(
                f"Failed to fetch feed {str(err)}", {"feed_id": feed_id, "url": url}
            )

        # parse protobuf
        feed = gtfs_realtime_pb2.FeedMessage()
        try:
            feed.ParseFromString(response.content)  # Parse the response content
        except protobuf.MessageError as err:
            raise ValidationError(
                f"Failed to parse GTFS-RT feed: {str(err)}", {"feed_id": feed_id}
            )

        return feed

    async def get_trip_updates(
        self,
        route_id: Optional[str] = None,
        feed_id: Optional[str] = None,
    ) -> List[Dict]:
        """
        Get trip updates from GTFS-RT feed.

        Args:
            route_id: Optional route ID (e.g., "A", "1", "B", etc.)
            feed_id: Optional feed ID (e.g., "gtfs-ace", "gtfs-bdfm", etc.)

        Returns:
            List of trip updates dictionaries.

        Example:
            >>> client = MTAClient()
            >>> updates = await client.get_trip_updates(route_id="A")
            >>> for update in updates:
            ...     print(update)
        """

        # Determine which feed to fetch
        if route_id and not feed_id:
            feed_id = self.get_feed_id_for_route(route_id)
            if not feed_id:
                raise ValidationError(
                    f"Unknown route ID: {route_id}", {"route_id": route_id}
                )

        if not feed_id:
            feed_id = "gtfs"  # Default to all lines feed

        # Fetch feed
        feed = await self.fetch_feed(feed_id)

        # Extract trip updates
        trip_updates = []
        for entity in feed.entity:
            if entity.HasField("trip_update"):
                trip_update = entity.trip_update
                trip_data = {
                    "trip_id": trip_update.trip.trip_id,
                    "route_id": trip_update.trip.route_id,
                    "start_time": (
                        trip_update.trip.start_time
                        if trip_update.trip.HasField("start_time")
                        else None
                    ),
                    "start_date": (
                        trip_update.trip.start_date
                        if trip_update.trip.HasField("start_date")
                        else None
                    ),
                    "stop_time_updates": [],
                }

                # Filter by route if specified
                if route_id and trip_data["route_id"].upper() != route_id.upper():
                    continue

                # Extract stop time updates
                for stu in trip_update.stop_time_update:
                    stop_data = {
                        "stop_id": stu.stop_id,
                        "arrival_time": None,
                        "departure_time": None,
                    }
                    if stu.HasField("arrival"):
                        stop_data["arrival_time"] = datetime.fromtimestamp(
                            stu.arrival.time
                        )
                    if stu.HasField("departure"):
                        stop_data["departure_time"] = datetime.fromtimestamp(
                            stu.departure.time
                        )

                    trip_data["stop_time_updates"].append(stop_data)

                trip_updates.append(trip_data)

        return trip_updates

    async def get_vehicle_positions(
        self,
        route_id: Optional[str] = None,
        feed_id: Optional[str] = None,
    ) -> List[Dict]:
        """
        Get vehicle positions from GTFS-RT feed.

        Args:
            route_id: Optional route ID to filter by
            feed_id: Optional feed ID

        Returns:
            List of vehicle position dictionaries

        Example:
            >>> client = MTAClient()
            >>> positions = await client.get_vehicle_positions(route_id="1")
            >>> for pos in positions:
            ...     print(f"Vehicle {pos['vehicle_id']} at stop {pos['stop_id']}")
        """
        # Determine which feed to fetch
        if route_id and not feed_id:
            feed_id = self.get_feed_id_for_route(route_id)

        if not feed_id:
            feed_id = "gtfs"

        # Fetch feed
        feed = await self.fetch_feed(feed_id)

        # Extract vehicle positions
        positions = []
        for entity in feed.entity:
            if entity.HasField("vehicle"):
                vehicle = entity.vehicle
                position_data = {
                    "vehicle_id": (
                        vehicle.vehicle.id if vehicle.vehicle.HasField("id") else None
                    ),
                    "trip_id": (
                        vehicle.trip.trip_id if vehicle.HasField("trip") else None
                    ),
                    "route_id": (
                        vehicle.trip.route_id if vehicle.HasField("trip") else None
                    ),
                    "stop_id": vehicle.stop_id if vehicle.HasField("stop_id") else None,
                    "current_status": (
                        vehicle.current_status
                        if vehicle.HasField("current_status")
                        else None
                    ),
                    "timestamp": (
                        datetime.fromtimestamp(vehicle.timestamp)
                        if vehicle.HasField("timestamp")
                        else None
                    ),
                }

                # Filter by route if specified
                if (
                    route_id
                    and position_data["route_id"]
                    and isinstance(position_data["route_id"], str)
                    and position_data["route_id"].upper() != route_id.upper()
                ):
                    continue

                positions.append(position_data)

        return positions


# Singleton instance
_mta_client: Optional[MTAClient] = None


def get_mta_client() -> MTAClient:
    """
    Get or create MTA client singleton instance.
    """

    global _mta_client
    if _mta_client is None:
        _mta_client = MTAClient()

    return _mta_client


async def close_mta_client():
    """Close the MTA client."""
    global _mta_client
    if _mta_client is not None:
        await _mta_client.close()
        _mta_client = None
