"""
Tests for authentication endpoints.

This module contains integration tests for:
- User registration
- User login
- Token generation and validation
"""

import pytest


@pytest.mark.asyncio
async def test_register_user(client, unique_email, unique_username):
    """Test user registration."""
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": unique_email,
            "username": unique_username,
            "password": "TestPass123!",
            "full_name": "New User",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == unique_email
    assert data["username"] == unique_username
    assert "id" in data
    assert "hashed_password" not in data


@pytest.mark.asyncio
async def test_register_duplicate_email(client, unique_username):
    """Test that duplicate email registration fails."""
    unique_email = "duplicate@test.com"
    
    # Register first user
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": unique_email,
            "username": unique_username,
            "password": "TestPass123!",
            "full_name": "Duplicate User",
        },
    )
    # Try to register with same email
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": unique_email,
            "username": "anotheruser",
            "password": "TestPass123!",
            "full_name": "Another User",
        },
    )
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_register_duplicate_username(client, unique_email):
    """Test that duplicate username registration fails."""
    unique_username = "uniqueuser"
    
    # Register first user
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": unique_email,
            "username": unique_username,
            "password": "TestPass123!",
            "full_name": "Unique User 1",
        },
    )
    # Try to register with same username
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "another@test.com",
            "username": unique_username,
            "password": "TestPass123!",
            "full_name": "Unique User 2",
        },
    )
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_login_success(client, unique_email, unique_username):
    """Test successful login."""
    # Register a user first
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": unique_email,
            "username": unique_username,
            "password": "LoginPass123!",
            "full_name": "Login User",
        },
    )
    # Login
    response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": unique_email,  # Note: email as username
            "password": "LoginPass123!",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_password(client, unique_email, unique_username):
    """Test that login with invalid password fails."""
    # Register a user first
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": unique_email,
            "username": unique_username,
            "password": "CorrectPass123!",
            "full_name": "Invalid Pass User",
        },
    )
    # Try to login with wrong password
    response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": unique_email,
            "password": "WrongPassword123!",
        },
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_login_nonexistent_user(client):
    """Test that login with non-existent user fails."""
    response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": "nonexistent@test.com",
            "password": "SomePassword123!",
        },
    )
    assert response.status_code == 401
