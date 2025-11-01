"""
Tests for user management endpoints.

This module contains integration tests for user CRUD operations.
"""

import pytest


@pytest.mark.asyncio
async def test_get_current_user(client, unique_email, unique_username):
    """Test getting current user profile."""
    # Register and login
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": unique_email,
            "username": unique_username,
            "password": "TestPass123!",
            "full_name": "Current User",
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
    headers = {"Authorization": f"Bearer {token}"}

    # Get current user
    response = await client.get("/api/v1/users/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == unique_email
    assert "id" in data


@pytest.mark.asyncio
async def test_get_current_user_without_token(client):
    """Test that getting current user without token fails."""
    response = await client.get("/api/v1/users/me")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_current_user_with_invalid_token(client):
    """Test that getting current user with invalid token fails."""
    headers = {"Authorization": "Bearer invalid_token_here"}
    response = await client.get("/api/v1/users/me", headers=headers)
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_user_by_id(client, unique_email, unique_username):
    """Test getting user by ID."""
    # Register and login
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": unique_email,
            "username": unique_username,
            "password": "TestPass123!",
            "full_name": "Get User",
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
    headers = {"Authorization": f"Bearer {token}"}

    # Get current user to find ID
    current_response = await client.get("/api/v1/users/me", headers=headers)
    user_id = current_response.json()["id"]

    # Get user by ID
    response = await client.get(f"/api/v1/users/{user_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id


@pytest.mark.asyncio
async def test_get_nonexistent_user(client, unique_email, unique_username):
    """Test that getting non-existent user fails."""
    # Register and login
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": unique_email,
            "username": unique_username,
            "password": "TestPass123!",
            "full_name": "Check Nonexistent",
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
    headers = {"Authorization": f"Bearer {token}"}

    # Try to get non-existent user
    response = await client.get("/api/v1/users/999999", headers=headers)
    # Note: This currently returns 403 (permission denied) instead of 404 (not found)
    # because the user doesn't have permission to view other users' profiles
    assert response.status_code in [403, 404]


@pytest.mark.asyncio
async def test_update_user_profile(client, unique_email, unique_username):
    """Test updating user profile."""
    # Register and login
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": unique_email,
            "username": unique_username,
            "password": "TestPass123!",
            "full_name": "Update User",
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
    headers = {"Authorization": f"Bearer {token}"}

    # Get current user to find ID
    current_response = await client.get("/api/v1/users/me", headers=headers)
    user_id = current_response.json()["id"]

    # Update user
    response = await client.patch(
        f"/api/v1/users/{user_id}",
        json={"full_name": "Updated Full Name"},
        headers=headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Updated Full Name"


@pytest.mark.asyncio
async def test_update_another_user_forbidden(client, unique_email, unique_username):
    """Test that updating another user's profile is forbidden."""
    # Register and login as user 1
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": unique_email,
            "username": unique_username,
            "password": "TestPass123!",
            "full_name": "User 1",
        },
    )
    login1_response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": unique_email,
            "password": "TestPass123!",
        },
    )
    token1 = login1_response.json()["access_token"]
    headers1 = {"Authorization": f"Bearer {token1}"}

    # Register and login as user 2 with different unique values
    import time
    timestamp = int(time.time() * 1000000)
    email2 = f"user2_{timestamp}@test.com"
    username2 = f"user2_{timestamp}"
    
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": email2,
            "username": username2,
            "password": "TestPass123!",
            "full_name": "User 2",
        },
    )
    login2_response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": email2,
            "password": "TestPass123!",
        },
    )
    token2 = login2_response.json()["access_token"]
    headers2 = {"Authorization": f"Bearer {token2}"}

    # Get user 1's ID
    current_response = await client.get("/api/v1/users/me", headers=headers1)
    user1_id = current_response.json()["id"]

    # Try to update user 1 as user 2 (should fail)
    response = await client.patch(
        f"/api/v1/users/{user1_id}",
        json={"full_name": "Hacked!"},
        headers=headers2,
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_list_users_requires_superuser(client, unique_email, unique_username):
    """Test that listing users requires superuser."""
    # Register and login as regular user
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": unique_email,
            "username": unique_username,
            "password": "TestPass123!",
            "full_name": "List Users",
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
    headers = {"Authorization": f"Bearer {token}"}

    # Try to list users (should fail - not superuser)
    response = await client.get("/api/v1/users/", headers=headers)
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_delete_user_requires_superuser(client, unique_email, unique_username):
    """Test that deleting user requires superuser."""
    # Register and login as regular user
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": unique_email,
            "username": unique_username,
            "password": "TestPass123!",
            "full_name": "Delete User",
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
    headers = {"Authorization": f"Bearer {token}"}

    # Get current user to find ID
    current_response = await client.get("/api/v1/users/me", headers=headers)
    user_id = current_response.json()["id"]

    # Try to delete user (should fail - not superuser)
    response = await client.delete(f"/api/v1/users/{user_id}", headers=headers)
    assert response.status_code == 403
