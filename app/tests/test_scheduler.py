"""
Tests for scheduler management endpoints and background tasks.

This module contains integration tests for:
- Scheduler status endpoints
- Job listing
- Scheduler pause/resume
- Authentication requirements
"""

import pytest
from unittest.mock import patch


@pytest.mark.asyncio
async def test_get_scheduler_status_requires_auth(client):
    """Test that scheduler status endpoint requires authentication."""
    response = await client.get("/api/v1/scheduler/status")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_list_jobs_requires_auth(client):
    """Test that list jobs endpoint requires authentication."""
    response = await client.get("/api/v1/scheduler/jobs")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_pause_scheduler_requires_auth(client):
    """Test that pause scheduler endpoint requires authentication."""
    response = await client.post("/api/v1/scheduler/pause")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_resume_scheduler_requires_auth(client):
    """Test that resume scheduler endpoint requires authentication."""
    response = await client.post("/api/v1/scheduler/resume")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_scheduler_status_requires_superuser(
    client, unique_email, unique_username
):
    """Test that scheduler status endpoint requires superuser."""
    # Register and login a regular user
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": unique_email,
            "username": unique_username,
            "password": "TestPass123!",
            "full_name": "Regular User",
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

    response = await client.get(
        "/api/v1/scheduler/status", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403  # Forbidden


@pytest.mark.asyncio
async def test_list_jobs_requires_superuser(client, unique_email, unique_username):
    """Test that list jobs endpoint requires superuser."""
    # Register and login a regular user
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": unique_email,
            "username": unique_username,
            "password": "TestPass123!",
            "full_name": "Regular User",
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

    response = await client.get(
        "/api/v1/scheduler/jobs", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403  # Forbidden


@pytest.mark.asyncio
async def test_list_jobs_success(client, unique_email, unique_username, test_db):
    """Test successful listing of scheduled jobs."""
    from app.services.user import UserService
    from app.schemas.user import UserCreate

    # Create a superuser
    superuser_data = UserCreate(
        email=unique_email,
        username=unique_username,
        password="TestPass123!",
        full_name="Super User",
        is_superuser=True,
    )
    superuser = await UserService.create_user(test_db, superuser_data)
    superuser.is_superuser = True
    test_db.add(superuser)
    await test_db.commit()
    await test_db.refresh(superuser)

    # Login as superuser
    login_response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": superuser.email,
            "password": "TestPass123!",
        },
    )
    token = login_response.json()["access_token"]

    # Mock scheduler jobs
    with patch(
        "app.api.v1.endpoints.scheduler.get_jobs",
        return_value=[
            {
                "id": "mta_refresh",
                "name": "MTA Data Refresh",
                "trigger": "interval[0:01:00]",
                "next_run_time": "2025-11-02T12:30:00Z",
            }
        ],
    ):
        response = await client.get(
            "/api/v1/scheduler/jobs", headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["id"] == "mta_refresh"


@pytest.mark.asyncio
async def test_get_scheduler_status_success(
    client, unique_email, unique_username, test_db
):
    """Test successful retrieval of scheduler status."""
    from app.services.user import UserService
    from app.schemas.user import UserCreate

    # Create a superuser
    superuser_data = UserCreate(
        email=unique_email,
        username=unique_username,
        password="TestPass123!",
        full_name="Super User",
        is_superuser=True,
    )
    superuser = await UserService.create_user(test_db, superuser_data)
    superuser.is_superuser = True
    test_db.add(superuser)
    await test_db.commit()
    await test_db.refresh(superuser)

    # Login as superuser
    login_response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": superuser.email,
            "password": "TestPass123!",
        },
    )
    token = login_response.json()["access_token"]

    # Mock scheduler status
    with patch(
        "app.api.v1.endpoints.scheduler.is_scheduler_running", return_value=True
    ), patch(
        "app.api.v1.endpoints.scheduler.get_jobs",
        return_value=[
            {
                "id": "mta_refresh",
                "name": "MTA Data Refresh",
                "trigger": "interval[0:01:00]",
                "next_run_time": "2025-11-02T12:30:00Z",
            }
        ],
    ):
        response = await client.get(
            "/api/v1/scheduler/status", headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["running"] is True
        assert data["jobs_count"] == 1


@pytest.mark.asyncio
async def test_pause_scheduler_success(client, unique_email, unique_username, test_db):
    """Test successful pausing of scheduler."""
    from app.services.user import UserService
    from app.schemas.user import UserCreate

    # Create a superuser
    superuser_data = UserCreate(
        email=unique_email,
        username=unique_username,
        password="TestPass123!",
        full_name="Super User",
        is_superuser=True,
    )
    superuser = await UserService.create_user(test_db, superuser_data)
    superuser.is_superuser = True
    test_db.add(superuser)
    await test_db.commit()
    await test_db.refresh(superuser)

    # Login as superuser
    login_response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": superuser.email,
            "password": "TestPass123!",
        },
    )
    token = login_response.json()["access_token"]

    with patch("app.api.v1.endpoints.scheduler.pause_scheduler") as mock_pause:
        response = await client.post(
            "/api/v1/scheduler/pause", headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        data = response.json()
        assert "Scheduler paused" in data["message"]
        mock_pause.assert_called_once()


@pytest.mark.asyncio
async def test_resume_scheduler_success(client, unique_email, unique_username, test_db):
    """Test successful resuming of scheduler."""
    from app.services.user import UserService
    from app.schemas.user import UserCreate

    # Create a superuser
    superuser_data = UserCreate(
        email=unique_email,
        username=unique_username,
        password="TestPass123!",
        full_name="Super User",
        is_superuser=True,
    )
    superuser = await UserService.create_user(test_db, superuser_data)
    superuser.is_superuser = True
    test_db.add(superuser)
    await test_db.commit()
    await test_db.refresh(superuser)

    # Login as superuser
    login_response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": superuser.email,
            "password": "TestPass123!",
        },
    )
    token = login_response.json()["access_token"]

    with patch("app.api.v1.endpoints.scheduler.resume_scheduler") as mock_resume:
        response = await client.post(
            "/api/v1/scheduler/resume", headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        data = response.json()
        assert "Scheduler resumed" in data["message"]
        mock_resume.assert_called_once()
