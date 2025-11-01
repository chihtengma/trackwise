"""
Pytest configuration and fixtures.

This module provides shared fixtures for all tests.
"""

import pytest
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
import time

from app.main import app


@pytest.fixture(scope="function")
def unique_email():
    """Generate a unique email for each test to avoid conflicts."""
    timestamp = int(time.time() * 1000000)  # Microsecond precision
    return f"test_{timestamp}@example.com"


@pytest.fixture(scope="function")
def unique_username():
    """Generate a unique username for each test to avoid conflicts."""
    timestamp = int(time.time() * 1000000)  # Microsecond precision
    return f"testuser_{timestamp}"


@pytest.fixture
async def client():
    """
    Create an async HTTP client for testing.

    Yields:
        AsyncClient: HTTP client configured for testing the app
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://test", timeout=30.0
    ) as client:
        yield client
