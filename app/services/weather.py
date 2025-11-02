"""
Weather service.

Business logic for weather data operations with caching.
"""

from app.core.cache import get_cache
from app.services.weather_client import get_weather_client
from app.schemas.weather import (
    WeatherResponse,
    WeatherCurrentResponse,
)


class WeatherService:
    """
    Service for weather operations.

    Handles weather queries, data transformation, and caching.
    """

    _cache_ttl_seconds = 300  # 5 minutes

    @staticmethod
    async def get_current_weather(
        location: str, units: str = "metric"
    ) -> WeatherCurrentResponse:
        """
        Get current weather for a location.

        Args:
            location: Location name or coordinates
            units: Temperature units ("metric", "imperial", or "kelvin")

        Returns:
            Simplified current weather response

        Example:
            >>> weather = await WeatherService.get_current_weather("New York")
            >>> print(f"Temperature: {weather.temp_celsius}°C")
        """
        # Check Redis cache
        cache_key = f"weather:{location}:{units}"
        cache = await get_cache()
        cached_data = await cache.get(cache_key)
        if cached_data:
            return WeatherCurrentResponse(**cached_data)

        # Fetch from API
        client = get_weather_client()
        raw_weather = await client.get_current_weather(location, units)

        # Parse response
        weather_response = WeatherResponse(**raw_weather)

        # Transform to simplified response
        main_data = weather_response.main
        weather_condition = weather_response.weather[0]

        # Convert temperature based on units
        if units == "imperial":
            temp_celsius = (main_data.temp - 32) * 5 / 9
            feels_like_celsius = (main_data.feels_like - 32) * 5 / 9
            temp_fahrenheit = main_data.temp
        elif units == "kelvin":
            temp_celsius = main_data.temp - 273.15
            feels_like_celsius = main_data.feels_like - 273.15
            temp_fahrenheit = (main_data.temp - 273.15) * 9 / 5 + 32
        else:  # metric
            temp_celsius = main_data.temp
            feels_like_celsius = main_data.feels_like
            temp_fahrenheit = main_data.temp * 9 / 5 + 32

        response = WeatherCurrentResponse(
            location=weather_response.name,
            temp_celsius=round(temp_celsius, 1),
            temp_fahrenheit=round(temp_fahrenheit, 1),
            feels_like_celsius=round(feels_like_celsius, 1),
            condition=weather_condition.main,
            description=weather_condition.description,
            humidity=main_data.humidity,
            wind_speed=weather_response.wind.speed,
            visibility_km=round(weather_response.visibility / 1000, 1),
        )

        # Cache the result in Redis
        await cache.set(
            cache_key,
            response.model_dump(),
            expiry_seconds=WeatherService._cache_ttl_seconds,
        )

        return response
