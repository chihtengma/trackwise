"""
Tests for transit endpoints.

This module contains integration tests for:
- Getting real-time trip updates
- Route queries
- Authentication requirements
"""

import pytest
from unittest.mock import patch, AsyncMock


@pytest.mark.asyncio
async def test_get_route_updates_requires_auth(client):
    """Test that route updates endpoint requires authentication."""
    response = await client.get("/api/v1/transit/routes/A/updates")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_query_routes_requires_auth(client):
    """Test that route query endpoint requires authentication."""
    response = await client.post(
        "/api/v1/transit/routes/query",
        json={
            "origin": "Times Sq-42 St",
            "destination": "Grand Central-42 St",
        },
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_route_updates_success(client, unique_email, unique_username):
    """Test successful trip updates retrieval."""
    # First, register and login
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

    # Mock the MTA client to avoid actual API calls
    mock_trip_updates = [
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
                }
            ],
        }
    ]

    with patch(
        "app.services.transit.TransitService.get_trip_updates_for_route",
        new_callable=AsyncMock,
    ) as mock_get:
        mock_get.return_value = mock_trip_updates

        response = await client.get(
            "/api/v1/transit/routes/A/updates",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["route_id"] == "A"
        assert data[0]["trip_id"] == "A-20241102-1"
        assert "stop_time_updates" in data[0]
        mock_get.assert_called_once_with(route_id="A")


@pytest.mark.asyncio
async def test_get_route_updates_different_routes(
    client, unique_email, unique_username
):
    """Test getting updates for different route IDs."""
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

    # Test different routes
    routes_to_test = ["1", "A", "N", "Q"]

    for route_id in routes_to_test:
        with patch(
            "app.services.transit.TransitService.get_trip_updates_for_route",
            new_callable=AsyncMock,
        ) as mock_get:
            mock_get.return_value = []

            response = await client.get(
                f"/api/v1/transit/routes/{route_id}/updates",
                headers={"Authorization": f"Bearer {token}"},
            )

            assert response.status_code == 200
            mock_get.assert_called_once_with(route_id=route_id)


@pytest.mark.asyncio
async def test_query_routes_success(client, unique_email, unique_username):
    """Test successful route query."""
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

    # Mock the transit service
    with patch(
        "app.services.transit.TransitService.query_routes",
        new_callable=AsyncMock,
    ) as mock_query:
        mock_query.return_value = {
            "query": {
                "origin": "Times Sq-42 St",
                "destination": "Grand Central-42 St",
                "max_routes": 3,
                "prefer_less_crowded": False,
            },
            "routes": [],
            "timestamp": "2024-11-02T12:00:00Z",
        }

        response = await client.post(
            "/api/v1/transit/routes/query",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "origin": "Times Sq-42 St",
                "destination": "Grand Central-42 St",
                "max_routes": 3,
                "prefer_less_crowded": False,
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert "query" in data
        assert "routes" in data
        assert "timestamp" in data
        assert data["query"]["origin"] == "Times Sq-42 St"
        assert data["query"]["destination"] == "Grand Central-42 St"
        mock_query.assert_called_once()


@pytest.mark.asyncio
async def test_query_routes_with_all_params(client, unique_email, unique_username):
    """Test route query with all optional parameters."""
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

    with patch(
        "app.services.transit.TransitService.query_routes",
        new_callable=AsyncMock,
    ) as mock_query:
        mock_query.return_value = {
            "query": {
                "origin": "Origin St",
                "destination": "Destination St",
                "departure_time": "2024-11-02T15:30:00Z",
                "max_routes": 5,
                "prefer_less_crowded": True,
            },
            "routes": [],
            "timestamp": "2024-11-02T12:00:00Z",
        }

        response = await client.post(
            "/api/v1/transit/routes/query",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "origin": "Origin St",
                "destination": "Destination St",
                "departure_time": "2024-11-02T15:30:00Z",
                "max_routes": 5,
                "prefer_less_crowded": True,
            },
        )

        assert response.status_code == 200
        mock_query.assert_called_once()


@pytest.mark.asyncio
async def test_query_routes_invalid_max_routes(client, unique_email, unique_username):
    """Test route query with invalid max_routes parameter."""
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

    # Test with max_routes > 10
    response = await client.post(
        "/api/v1/transit/routes/query",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "origin": "Origin St",
            "destination": "Destination St",
            "max_routes": 15,
        },
    )
    assert response.status_code == 422  # Validation error

    # Test with max_routes < 1
    response = await client.post(
        "/api/v1/transit/routes/query",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "origin": "Origin St",
            "destination": "Destination St",
            "max_routes": 0,
        },
    )
    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_query_routes_missing_required_fields(
    client, unique_email, unique_username
):
    """Test route query with missing required fields."""
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

    # Missing destination
    response = await client.post(
        "/api/v1/transit/routes/query",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "origin": "Origin St",
        },
    )
    assert response.status_code == 422  # Validation error

    # Missing origin
    response = await client.post(
        "/api/v1/transit/routes/query",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "destination": "Destination St",
        },
    )
    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_query_routes_with_weather(client, unique_email, unique_username):
    """Test route query with weather integration."""
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

    # Mock weather service
    mock_weather = {
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
    ) as mock_weather_service, patch(
        "app.services.transit.TransitService.query_routes",
        new_callable=AsyncMock,
    ) as mock_query:
        mock_weather_service.return_value = mock_weather
        mock_query.return_value = {
            "query": {
                "origin": "Times Sq-42 St",
                "destination": "Grand Central-42 St",
                "max_routes": 3,
                "prefer_less_crowded": False,
                "include_weather": True,
                "weather_location": "New York",
            },
            "routes": [],
            "timestamp": "2024-11-02T12:00:00Z",
            "weather": mock_weather,
        }

        response = await client.post(
            "/api/v1/transit/routes/query",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "origin": "Times Sq-42 St",
                "destination": "Grand Central-42 St",
                "max_routes": 3,
                "prefer_less_crowded": False,
                "include_weather": True,
                "weather_location": "New York",
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert "weather" in data
        assert data["weather"]["location"] == "New York"
        assert data["weather"]["temp_celsius"] == 15.0
        mock_query.assert_called_once()


@pytest.mark.asyncio
async def test_query_routes_without_weather_flag(client, unique_email, unique_username):
    """Test route query without weather flag returns no weather."""
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

    with patch(
        "app.services.transit.TransitService.query_routes",
        new_callable=AsyncMock,
    ) as mock_query:
        mock_query.return_value = {
            "query": {
                "origin": "Times Sq-42 St",
                "destination": "Grand Central-42 St",
                "max_routes": 3,
                "prefer_less_crowded": False,
                "include_weather": False,
                "weather_location": None,
            },
            "routes": [],
            "timestamp": "2024-11-02T12:00:00Z",
            "weather": None,
        }

        response = await client.post(
            "/api/v1/transit/routes/query",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "origin": "Times Sq-42 St",
                "destination": "Grand Central-42 St",
                "max_routes": 3,
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data.get("weather") is None
        mock_query.assert_called_once()
