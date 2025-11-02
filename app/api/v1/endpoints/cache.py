"""
Cache management endpoints.

This module provides endpoints for managing the Redis cache.
"""

from typing import Dict

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_current_active_user, get_current_superuser
from app.core.cache import get_cache
from app.models.user import User

router = APIRouter()


@router.get("/stats", response_model=Dict)
async def get_cache_stats(current_user: User = Depends(get_current_active_user)):
    """
    Get cache statistics.

    Returns information about the Redis cache including
    connection status, key count, and memory usage.

    Args:
        current_user: Current authenticated user

    Returns:
        Cache statistics dictionary

    Example Request:
        GET /api/v1/cache/stats
        Authorization: Bearer <token>

    Example Response:
        {
            "connected": true,
            "keys_count": 42,
            "used_memory_human": "1.5M"
        }
    """
    cache = await get_cache()
    stats = await cache.get_stats()
    return stats


@router.post("/clear")
async def clear_cache(
    current_user: User = Depends(get_current_superuser),
):
    """
    Clear all cache data.

    Requires superuser privileges.

    Args:
        current_user: Current authenticated superuser

    Returns:
        Success message

    Example Request:
        POST /api/v1/cache/clear
        Authorization: Bearer <token>

    Example Response:
        {
            "message": "Cache cleared successfully"
        }
    """
    cache = await get_cache()
    success = await cache.clear_all()
    if success:
        return {"message": "Cache cleared successfully"}
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Failed to clear cache",
    )


@router.delete("/pattern/{pattern:path}")
async def clear_cache_pattern(
    pattern: str,
    current_user: User = Depends(get_current_superuser),
):
    """
    Clear cache keys matching a pattern.

    Requires superuser privileges.

    Args:
        pattern: Redis key pattern (e.g., "weather:*", "transit:*")
        current_user: Current authenticated superuser

    Returns:
        Success message with count of deleted keys

    Example Request:
        DELETE /api/v1/cache/pattern/weather:*
        Authorization: Bearer <token>

    Example Response:
        {
            "message": "Deleted 5 keys matching pattern weather:*"
        }
    """
    cache = await get_cache()
    count = await cache.delete_pattern(pattern)
    return {"message": f"Deleted {count} keys matching pattern {pattern}"}
