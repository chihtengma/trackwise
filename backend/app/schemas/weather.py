"""
Weather data schemas.

Pydantic models for OpenWeatherMap data structures.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class WeatherCondition(BaseModel):
    """
    Weather condition information.
    """

    id: int = Field(..., description="Weather condition ID")
    main: str = Field(..., description="Weather condition (Rain, Clear, etc.)")
    description: str = Field(..., description="Detailed weather description")
    icon: str = Field(..., description="Weather icon code")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 800,
                "main": "Clear",
                "description": "clear sky",
                "icon": "01d",
            }
        }
    }


class MainWeather(BaseModel):
    """
    Main weather parameters.
    """

    temp: float = Field(..., description="Temperature in Kelvin")
    feels_like: float = Field(..., description="Feels-like temperature in Kelvin")
    temp_min: float = Field(..., description="Minimum temperature in Kelvin")
    temp_max: float = Field(..., description="Maximum temperature in Kelvin")
    pressure: int = Field(..., description="Atmospheric pressure in hPa")
    humidity: int = Field(..., description="Humidity percentage (0-100)")

    model_config = {
        "json_schema_extra": {
            "example": {
                "temp": 288.15,
                "feels_like": 287.85,
                "temp_min": 286.15,
                "temp_max": 290.15,
                "pressure": 1013,
                "humidity": 65,
            }
        }
    }


class Wind(BaseModel):
    """
    Wind information.
    """

    speed: float = Field(..., description="Wind speed in m/s")
    deg: int = Field(..., description="Wind direction in degrees (0-360)")
    gust: Optional[float] = Field(None, description="Wind gust speed in m/s")

    model_config = {
        "json_schema_extra": {"example": {"speed": 4.5, "deg": 270, "gust": 6.2}}
    }


class Clouds(BaseModel):
    """
    Cloud coverage information.
    """

    all: int = Field(..., description="Cloud coverage percentage (0-100)")

    model_config = {"json_schema_extra": {"example": {"all": 20}}}


class Precipitation(BaseModel):
    """
    Precipitation information (rain or snow).
    """

    one_hour: Optional[float] = Field(
        None,
        alias="1h",
        description="Precipitation volume for last 1 hour in mm",
    )
    three_hours: Optional[float] = Field(
        None,
        alias="3h",
        description="Precipitation volume for last 3 hours in mm",
    )

    model_config = {"json_schema_extra": {"example": {"1h": 2.5, "3h": 5.0}}}


class WeatherResponse(BaseModel):
    """
    Current weather response from OpenWeatherMap.
    """

    coord: dict = Field(..., description="Coordinates (lat, lon)")
    weather: List[WeatherCondition] = Field(..., description="Weather conditions list")
    base: str = Field(..., description="Internal parameter")
    main: MainWeather = Field(..., description="Main weather parameters")
    visibility: int = Field(..., description="Visibility in meters")
    wind: Wind = Field(..., description="Wind information")
    clouds: Clouds = Field(..., description="Cloud coverage")
    dt: int = Field(..., description="Time of data calculation (Unix timestamp)")
    sys: dict = Field(..., description="System information")
    timezone: int = Field(..., description="Timezone offset in seconds from UTC")
    id: int = Field(..., description="City ID")
    name: str = Field(..., description="City name")
    cod: int = Field(..., description="Internal parameter")

    model_config = {
        "json_schema_extra": {
            "example": {
                "coord": {"lon": -73.9687, "lat": 40.7589},
                "weather": [
                    {
                        "id": 800,
                        "main": "Clear",
                        "description": "clear sky",
                        "icon": "01d",
                    }
                ],
                "base": "stations",
                "main": {
                    "temp": 288.15,
                    "feels_like": 287.85,
                    "temp_min": 286.15,
                    "temp_max": 290.15,
                    "pressure": 1013,
                    "humidity": 65,
                },
                "visibility": 10000,
                "wind": {"speed": 4.5, "deg": 270},
                "clouds": {"all": 20},
                "dt": 1698969600,
                "sys": {
                    "type": 2,
                    "id": 2015123,
                    "country": "US",
                    "sunrise": 1698924600,
                    "sunset": 1698961200,
                },
                "timezone": -18000,
                "id": 5128581,
                "name": "New York",
                "cod": 200,
            }
        }
    }


class WeatherQuery(BaseModel):
    """
    Request schema for weather queries.
    """

    location: str = Field(
        ...,
        description=(
            "Location name or coordinates (e.g., 'New York' or '40.7128,-74.0060')"
        ),
    )

    model_config = {"json_schema_extra": {"example": {"location": "New York"}}}


class WeatherCurrentResponse(BaseModel):
    """
    Simplified current weather response.
    """

    location: str = Field(..., description="Location name")
    temp_celsius: float = Field(..., description="Temperature in Celsius")
    temp_fahrenheit: float = Field(..., description="Temperature in Fahrenheit")
    feels_like_celsius: float = Field(
        ..., description="Feels-like temperature in Celsius"
    )
    condition: str = Field(..., description="Weather condition")
    description: str = Field(..., description="Detailed weather description")
    humidity: int = Field(..., description="Humidity percentage")
    wind_speed: float = Field(..., description="Wind speed in m/s")
    visibility_km: float = Field(..., description="Visibility in kilometers")

    model_config = {
        "json_schema_extra": {
            "example": {
                "location": "New York",
                "temp_celsius": 15.0,
                "temp_fahrenheit": 59.0,
                "feels_like_celsius": 14.7,
                "condition": "Clear",
                "description": "clear sky",
                "humidity": 65,
                "wind_speed": 4.5,
                "visibility_km": 10.0,
            }
        }
    }
