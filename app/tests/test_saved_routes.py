"""
Tests for saved routes endpoints.

This module contains integration tests for:
- Creating saved routes
- Listing saved routes
- Getting specific routes
- Updating saved routes
- Deleting saved routes
- Authentication requirements
- Favorites filtering
"""

import pytest


@pytest.mark.asyncio
async def test_create_saved_route_requires_auth(client):
    """Test that creating a saved route requires authentication."""
    response = await client.post(
        "/api/v1/saved-routes/",
        json={
            "name": "Home to Work",
            "origin": "Times Sq-42 St",
            "destination": "Grand Central-42 St",
        },
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_list_saved_routes_requires_auth(client):
    """Test that listing saved routes requires authentication."""
    response = await client.get("/api/v1/saved-routes/")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_saved_route_requires_auth(client):
    """Test that getting a saved route requires authentication."""
    response = await client.get("/api/v1/saved-routes/1")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_update_saved_route_requires_auth(client):
    """Test that updating a saved route requires authentication."""
    response = await client.put("/api/v1/saved-routes/1", json={"name": "Updated Name"})
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_delete_saved_route_requires_auth(client):
    """Test that deleting a saved route requires authentication."""
    response = await client.delete("/api/v1/saved-routes/1")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_saved_route_success(client, unique_email, unique_username):
    """Test successful creation of a saved route."""
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

    # Create saved route
    response = await client.post(
        "/api/v1/saved-routes/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Home to Work",
            "origin": "Times Sq-42 St",
            "destination": "Grand Central-42 St",
            "route_types": "subway",
            "notes": "My morning commute",
            "is_favorite": True,
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Home to Work"
    assert data["origin"] == "Times Sq-42 St"
    assert data["destination"] == "Grand Central-42 St"
    assert data["is_favorite"] is True
    assert "id" in data
    assert data["user_id"] is not None


@pytest.mark.asyncio
async def test_list_saved_routes_success(client, unique_email, unique_username):
    """Test successful listing of saved routes."""
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

    # List routes (should be empty initially)
    response = await client.get(
        "/api/v1/saved-routes/", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "routes" in data
    assert "total" in data
    assert "favorites_count" in data
    assert isinstance(data["routes"], list)
    assert data["total"] == 0
    assert data["favorites_count"] == 0


@pytest.mark.asyncio
async def test_list_saved_routes_with_favorites(client, unique_email, unique_username):
    """Test listing routes with favorites only filter."""
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

    # Create a favorite and a non-favorite route
    await client.post(
        "/api/v1/saved-routes/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Favorite Route",
            "origin": "A",
            "destination": "B",
            "is_favorite": True,
        },
    )
    await client.post(
        "/api/v1/saved-routes/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Regular Route",
            "origin": "C",
            "destination": "D",
            "is_favorite": False,
        },
    )

    # List only favorites
    response = await client.get(
        "/api/v1/saved-routes/?favorites_only=true",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    # All returned routes should be favorites
    for route in data["routes"]:
        assert route["is_favorite"] is True


@pytest.mark.asyncio
async def test_get_saved_route_success(client, unique_email, unique_username):
    """Test successful retrieval of a specific saved route."""
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

    # Create a route
    create_response = await client.post(
        "/api/v1/saved-routes/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Test Route",
            "origin": "Origin Stop",
            "destination": "Destination Stop",
        },
    )
    route_id = create_response.json()["id"]

    # Get the route
    response = await client.get(
        f"/api/v1/saved-routes/{route_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == route_id
    assert data["name"] == "Test Route"


@pytest.mark.asyncio
async def test_get_nonexistent_route(client, unique_email, unique_username):
    """Test getting a route that doesn't exist."""
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

    # Try to get a non-existent route
    response = await client.get(
        "/api/v1/saved-routes/99999",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_saved_route_success(client, unique_email, unique_username):
    """Test successful update of a saved route."""
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

    # Create a route
    create_response = await client.post(
        "/api/v1/saved-routes/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Original Name",
            "origin": "Origin",
            "destination": "Destination",
            "is_favorite": False,
        },
    )
    route_id = create_response.json()["id"]

    # Update the route
    response = await client.put(
        f"/api/v1/saved-routes/{route_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Updated Name",
            "is_favorite": True,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Name"
    assert data["is_favorite"] is True
    # Other fields should remain unchanged
    assert data["origin"] == "Origin"
    assert data["destination"] == "Destination"


@pytest.mark.asyncio
async def test_delete_saved_route_success(client, unique_email, unique_username):
    """Test successful deletion of a saved route."""
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

    # Create a route
    create_response = await client.post(
        "/api/v1/saved-routes/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "To Delete",
            "origin": "Origin",
            "destination": "Destination",
        },
    )
    route_id = create_response.json()["id"]

    # Delete the route
    response = await client.delete(
        f"/api/v1/saved-routes/{route_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 204

    # Verify it's deleted
    get_response = await client.get(
        f"/api/v1/saved-routes/{route_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_user_cannot_access_other_users_routes(
    client, unique_email, unique_username
):
    """Test that users cannot access other users' saved routes."""
    # Create first user and route
    email1 = unique_email
    username1 = unique_username
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": email1,
            "username": username1,
            "password": "TestPass123!",
            "full_name": "User 1",
        },
    )
    login1 = await client.post(
        "/api/v1/auth/login",
        data={"username": email1, "password": "TestPass123!"},
    )
    token1 = login1.json()["access_token"]

    create_resp = await client.post(
        "/api/v1/saved-routes/",
        headers={"Authorization": f"Bearer {token1}"},
        json={
            "name": "User 1 Route",
            "origin": "A",
            "destination": "B",
        },
    )
    route_id = create_resp.json()["id"]

    # Create second user
    import time

    email2 = f"user2_{int(time.time() * 1000000)}@example.com"
    username2 = f"user2_{int(time.time() * 1000000)}"
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": email2,
            "username": username2,
            "password": "TestPass123!",
            "full_name": "User 2",
        },
    )
    login2 = await client.post(
        "/api/v1/auth/login",
        data={"username": email2, "password": "TestPass123!"},
    )
    token2 = login2.json()["access_token"]

    # Try to access user1's route with user2's token
    response = await client.get(
        f"/api/v1/saved-routes/{route_id}",
        headers={"Authorization": f"Bearer {token2}"},
    )

    assert response.status_code == 404
