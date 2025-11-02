"""
Tests for cache management endpoints.

This module contains integration tests for:
- Cache statistics endpoint
- Cache clearing
- Cache pattern deletion
- Authentication requirements
"""

import pytest
from unittest.mock import patch, AsyncMock


@pytest.mark.asyncio
async def test_get_cache_stats_requires_auth(client):
    """Test that cache stats endpoint requires authentication."""
    response = await client.get("/api/v1/cache/stats")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_clear_cache_requires_auth(client):
    """Test that clear cache endpoint requires authentication."""
    response = await client.post("/api/v1/cache/clear")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_cache_stats_success(client, unique_email, unique_username):
    """Test successful cache stats retrieval."""
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

    # Mock cache stats
    mock_stats = {
        "connected": True,
        "keys_count": 42,
        "used_memory_human": "1.5M",
    }

    with patch(
        "app.api.v1.endpoints.cache.get_cache", new_callable=AsyncMock
    ) as mock_get:
        mock_cache = AsyncMock()
        mock_cache.get_stats = AsyncMock(return_value=mock_stats)
        mock_get.return_value = mock_cache

        response = await client.get(
            "/api/v1/cache/stats",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["connected"] is True
        assert "keys_count" in data


@pytest.mark.asyncio
async def test_get_cache_stats_not_connected(client, unique_email, unique_username):
    """Test cache stats when Redis is not connected."""
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

    # Mock cache stats when not connected
    mock_stats = {
        "connected": False,
        "message": "Redis not connected",
    }

    with patch(
        "app.api.v1.endpoints.cache.get_cache", new_callable=AsyncMock
    ) as mock_get:
        mock_cache = AsyncMock()
        mock_cache.get_stats = AsyncMock(return_value=mock_stats)
        mock_get.return_value = mock_cache

        response = await client.get(
            "/api/v1/cache/stats",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["connected"] is False
        assert "message" in data


@pytest.mark.asyncio
async def test_clear_cache_success(client, unique_email, unique_username, test_db):
    """Test successful cache clearing (requires superuser)."""
    from app.services.user import UserService
    from app.schemas.user import UserCreate

    # Create a superuser
    superuser_data = UserCreate(
        email=unique_email,
        username=unique_username,
        password="TestPass123!",
        full_name="Super User",
    )
    superuser = await UserService.create_user(test_db, superuser_data)
    superuser.is_superuser = True
    test_db.add(superuser)
    await test_db.commit()
    await test_db.refresh(superuser)

    # Get token
    login_response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": unique_email,
            "password": "TestPass123!",
        },
    )
    token = login_response.json()["access_token"]

    # Mock cache clear
    with patch(
        "app.api.v1.endpoints.cache.get_cache", new_callable=AsyncMock
    ) as mock_get:
        mock_cache = AsyncMock()
        mock_cache.clear_all = AsyncMock(return_value=True)
        mock_get.return_value = mock_cache

        response = await client.post(
            "/api/v1/cache/clear",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert "message" in data


@pytest.mark.asyncio
async def test_clear_cache_requires_superuser(client, unique_email, unique_username):
    """Test that clear cache requires superuser."""
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

    # Try to clear cache as non-superuser
    response = await client.post(
        "/api/v1/cache/clear",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 403  # Forbidden


@pytest.mark.asyncio
async def test_clear_cache_pattern_success(
    client, unique_email, unique_username, test_db
):
    """Test successful cache pattern deletion (requires superuser)."""
    from app.services.user import UserService
    from app.schemas.user import UserCreate

    # Create a superuser
    superuser_data = UserCreate(
        email=unique_email,
        username=unique_username,
        password="TestPass123!",
        full_name="Super User",
    )
    superuser = await UserService.create_user(test_db, superuser_data)
    superuser.is_superuser = True
    test_db.add(superuser)
    await test_db.commit()
    await test_db.refresh(superuser)

    # Get token
    login_response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": unique_email,
            "password": "TestPass123!",
        },
    )
    token = login_response.json()["access_token"]

    # Mock cache pattern deletion
    with patch(
        "app.api.v1.endpoints.cache.get_cache", new_callable=AsyncMock
    ) as mock_get:
        mock_cache = AsyncMock()
        mock_cache.delete_pattern = AsyncMock(return_value=5)
        mock_get.return_value = mock_cache

        response = await client.delete(
            "/api/v1/cache/pattern/weather:*",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "5" in data["message"]


@pytest.mark.asyncio
async def test_clear_cache_pattern_requires_superuser(
    client, unique_email, unique_username
):
    """Test that clear cache pattern requires superuser."""
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

    # Try to delete pattern as non-superuser
    response = await client.delete(
        "/api/v1/cache/pattern/weather:*",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 403  # Forbidden
