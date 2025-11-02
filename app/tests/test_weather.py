"""
Tests for weather endpoints.

This module contains integration tests for:
- Getting current weather
- Weather queries
- Authentication requirements
- Different unit systems
"""

import pytest
from unittest.mock import patch, AsyncMock


@pytest.mark.asyncio
async def test_get_current_weather_requires_auth(client):
    """Test that weather endpoint requires authentication."""
    response = await client.get("/api/v1/weather/current?location=New York")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_query_weather_requires_auth(client):
    """Test that weather query endpoint requires authentication."""
    response = await client.post(
        "/api/v1/weather/query",
        json={"location": "New York"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_current_weather_success(client, unique_email, unique_username):
    """Test successful weather retrieval."""
    # Register and login
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": unique_email,
            "username": unique_username,
            "password": "TestPass123!",
            "full_name": "Test User",
        },
    )
    login_response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": unique_email,  # Note: email as username
            "password": "TestPass123!",
        },
    )
    token = login_response.json()["access_token"]

    # Mock the weather client
    mock_weather_data = {
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

    with patch(
        "app.services.weather.WeatherService.get_current_weather",
        new_callable=AsyncMock,
    ) as mock_get:
        mock_get.return_value = mock_weather_data

        response = await client.get(
            "/api/v1/weather/current?location=New+York&units=metric",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["location"] == "New York"
        assert data["temp_celsius"] == 15.0
        assert data["condition"] == "Clear"
        assert "humidity" in data
        mock_get.assert_called_once_with("New York", "metric")


@pytest.mark.asyncio
async def test_get_current_weather_imperial_units(
    client, unique_email, unique_username
):
    """Test weather retrieval with imperial units."""
    # Register and login
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": unique_email,
            "username": unique_username,
            "password": "TestPass123!",
            "full_name": "Test User",
        },
    )
    login_response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": unique_email,
            "password": "TestPass123!",
        },
    )
    token = login_response.json()["access_token"]

    mock_weather_data = {
        "location": "New York",
        "temp_celsius": 15.0,
        "temp_fahrenheit": 59.0,
        "feels_like_celsius": 14.7,
        "condition": "Rain",
        "description": "light rain",
        "humidity": 80,
        "wind_speed": 6.0,
        "visibility_km": 8.0,
    }

    with patch(
        "app.services.weather.WeatherService.get_current_weather",
        new_callable=AsyncMock,
    ) as mock_get:
        mock_get.return_value = mock_weather_data

        response = await client.get(
            "/api/v1/weather/current?location=New+York&units=imperial",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert "temp_fahrenheit" in data
        mock_get.assert_called_once_with("New York", "imperial")


@pytest.mark.asyncio
async def test_query_weather_success(client, unique_email, unique_username):
    """Test successful weather query via POST."""
    # Register and login
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": unique_email,
            "username": unique_username,
            "password": "TestPass123!",
            "full_name": "Test User",
        },
    )
    login_response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": unique_email,
            "password": "TestPass123!",
        },
    )
    token = login_response.json()["access_token"]

    mock_weather_data = {
        "location": "London",
        "temp_celsius": 10.0,
        "temp_fahrenheit": 50.0,
        "feels_like_celsius": 9.5,
        "condition": "Clouds",
        "description": "scattered clouds",
        "humidity": 70,
        "wind_speed": 3.5,
        "visibility_km": 10.0,
    }

    with patch(
        "app.services.weather.WeatherService.get_current_weather",
        new_callable=AsyncMock,
    ) as mock_get:
        mock_get.return_value = mock_weather_data

        response = await client.post(
            "/api/v1/weather/query?units=metric",
            headers={"Authorization": f"Bearer {token}"},
            json={"location": "London"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["location"] == "London"
        assert "condition" in data
        assert "humidity" in data
        mock_get.assert_called_once_with("London", "metric")


@pytest.mark.asyncio
async def test_query_weather_different_locations(client, unique_email, unique_username):
    """Test weather query for different locations."""
    # Register and login
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": unique_email,
            "username": unique_username,
            "password": "TestPass123!",
            "full_name": "Test User",
        },
    )
    login_response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": unique_email,
            "password": "TestPass123!",
        },
    )
    token = login_response.json()["access_token"]

    locations = ["Tokyo", "Paris", "Sydney"]

    for location in locations:
        with patch(
            "app.services.weather.WeatherService.get_current_weather",
            new_callable=AsyncMock,
        ) as mock_get:
            mock_weather_data = {
                "location": location,
                "temp_celsius": 20.0,
                "temp_fahrenheit": 68.0,
                "feels_like_celsius": 19.5,
                "condition": "Clear",
                "description": "clear sky",
                "humidity": 60,
                "wind_speed": 3.0,
                "visibility_km": 10.0,
            }
            mock_get.return_value = mock_weather_data

            response = await client.get(
                f"/api/v1/weather/current?location={location}",
                headers={"Authorization": f"Bearer {token}"},
            )

            assert response.status_code == 200
            data = response.json()
            assert data["location"] == location
            mock_get.assert_called_once_with(location, "metric")


@pytest.mark.asyncio
async def test_query_weather_all_unit_systems(client, unique_email, unique_username):
    """Test weather query with all unit systems."""
    # Register and login
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": unique_email,
            "username": unique_username,
            "password": "TestPass123!",
            "full_name": "Test User",
        },
    )
    login_response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": unique_email,
            "password": "TestPass123!",
        },
    )
    token = login_response.json()["access_token"]

    units_to_test = ["metric", "imperial", "kelvin"]

    for units in units_to_test:
        with patch(
            "app.services.weather.WeatherService.get_current_weather",
            new_callable=AsyncMock,
        ) as mock_get:
            mock_weather_data = {
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
            mock_get.return_value = mock_weather_data

            response = await client.get(
                f"/api/v1/weather/current?location=New+York&units={units}",
                headers={"Authorization": f"Bearer {token}"},
            )

            assert response.status_code == 200
            mock_get.assert_called_once_with("New York", units)
