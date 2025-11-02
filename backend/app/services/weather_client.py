"""
OpenWeather API Client.

Service for fetching weather data from OpenWeatherMap API.
"""

import httpx
from typing import Optional, Dict

from app.core.config import settings
from app.core.exceptions import ValidationError


class WeatherClient:
    """
    Client for OpenWeatherMap API.

    Handles fetching weather data from OpenWeatherMap.
    """

    def __init__(self):
        """Initialize the weather client."""
        self.base_url = settings.OPENWEATHER_BASE_URL
        self.api_key = settings.OPENWEATHER_API_KEY
        self.client = httpx.AsyncClient(timeout=30.0)

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()

    async def get_current_weather(
        self,
        location: str,
        units: str = "metric",
    ) -> Dict:
        """
        Get current weather for a location.

        Args:
            location: Location name (e.g., "New York") or coordinates
            units: Temperature units ("metric", "imperial", or "kelvin")

        Returns:
            Weather data dictionary from OpenWeatherMap

        Raises:
            ValidationError: If weather cannot be fetched

        Example:
            >>> client = WeatherClient()
            >>> weather = await client.get_current_weather("New York")
            >>> print(f"Temperature: {weather['main']['temp']}°C")
        """
        url = f"{self.base_url}/weather"
        params = {
            "q": location,
            "appid": self.api_key,
            "units": units,
        }

        try:
            response = await self.client.get(url, params=params)
            response.raise_for_status()
        except httpx.HTTPStatusError as err:
            if err.response.status_code == 404:
                raise ValidationError(
                    f"Location not found: {location}",
                    {"location": location},
                )
            elif err.response.status_code == 401:
                raise ValidationError(
                    "Invalid API key for OpenWeatherMap",
                    {"api_key": "invalid"},
                )
            raise ValidationError(
                f"Failed to fetch weather: {str(err)}",
                {"location": location},
            )
        except httpx.HTTPError as err:
            raise ValidationError(
                f"Failed to fetch weather: {str(err)}",
                {"location": location},
            )

        return response.json()


# Singleton instance
_weather_client: Optional[WeatherClient] = None


def get_weather_client() -> WeatherClient:
    """
    Get or create weather client singleton instance.
    """

    global _weather_client
    if _weather_client is None:
        _weather_client = WeatherClient()

    return _weather_client


async def close_weather_client():
    """Close the weather client."""
    global _weather_client
    if _weather_client is not None:
        await _weather_client.close()
        _weather_client = None
