"""
Pytest configuration and fixtures.

This module provides shared fixtures for all tests.
"""

import pytest
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
import time
import os
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from app.core.database import Base, get_async_db
from app.main import app

# Set test environment variables before importing app
# Use a real PostgreSQL database URL format to avoid SQLite pool issues
os.environ.setdefault("ENVIRONMENT", "development")
os.environ.setdefault(
    "DATABASE_URL", "postgresql://test:test@localhost:5432/trackwise_test"
)
os.environ.setdefault("SECRET_KEY", "test-secret-key-" + "x" * 40)
os.environ.setdefault("OPENWEATHER_API_KEY", "test-api-key")


# Test database setup using SQLite with async support
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop():
    """Create an event loop for pytest-asyncio."""
    import asyncio

    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_engine():
    """Create a test async engine with in-memory SQLite database."""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        connect_args={"check_same_thread": False},
    )

    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    # Cleanup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.fixture(scope="session")
def test_session_factory(test_engine):
    """Create a test session factory."""
    return async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )


@pytest.fixture
async def test_db(test_session_factory) -> AsyncGenerator[AsyncSession, None]:
    """
    Provide a test database session.

    Each test gets a fresh transaction that's rolled back after the test.
    """
    async with test_session_factory() as session:
        yield session
        await session.rollback()


@pytest.fixture
def override_get_db(test_db):
    """Override the get_async_db dependency with test database."""

    async def _get_test_db():
        yield test_db

    return _get_test_db


@pytest.fixture
async def client(override_get_db):
    """
    Create an async HTTP client for testing.

    Yields:
        AsyncClient: HTTP client configured for testing the app
    """
    # Override the database dependency
    app.dependency_overrides[get_async_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://test", timeout=30.0
    ) as client:
        yield client

    # Clear dependency overrides
    app.dependency_overrides.clear()


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
