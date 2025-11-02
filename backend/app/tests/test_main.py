"""
Tests for main application endpoints.

This module contains tests for general application endpoints.
"""

import pytest


@pytest.mark.asyncio
async def test_root_endpoint(client):
    """Test root endpoint."""
    response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "status" in data
    assert data["status"] == "operational"


@pytest.mark.asyncio
async def test_health_check(client):
    """Test health check endpoint."""
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    # Status can be "healthy" or "degraded" depending on dependencies
    assert data["status"] in ["healthy", "degraded"]
    assert "environment" in data
    assert "version" in data


@pytest.mark.asyncio
async def test_404_handler(client):
    """Test custom 404 handler."""
    response = await client.get("/nonexistent-endpoint")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "path" in data


@pytest.mark.asyncio
async def test_openapi_schema(client):
    """Test that OpenAPI schema is accessible."""
    response = await client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert "openapi" in data
    assert "info" in data
    assert "paths" in data
