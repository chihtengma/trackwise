"""
Redis cache service.

Provides centralized caching functionality with Redis.
"""

import json
from typing import Optional, Any

import redis.asyncio as redis
from redis.asyncio import Redis

from app.core.config import settings


class CacheService:
    """
    Redis cache service for application-wide caching.

    Provides methods for getting, setting, and managing cached data.
    """

    def __init__(self):
        """Initialize the cache service."""
        self.redis_client: Optional[Redis] = None
        self.is_connected = False

    async def connect(self):
        """Connect to Redis server."""
        if not self.is_connected:
            try:
                self.redis_client = redis.from_url(
                    settings.REDIS_URL,
                    encoding="utf-8",
                    decode_responses=True,
                )
                # Test connection
                await self.redis_client.ping()
                self.is_connected = True
            except Exception:
                # If Redis is not available, continue without it
                self.is_connected = False
                self.redis_client = None

    async def disconnect(self):
        """Disconnect from Redis server."""
        if self.redis_client:
            await self.redis_client.close()
            self.is_connected = False
            self.redis_client = None

    async def get(self, key: str) -> Optional[Any]:
        """
        Get a value from cache.

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found
        """
        if not self.is_connected or not self.redis_client:
            return None

        try:
            value = await self.redis_client.get(key)
            if value:
                return json.loads(value)
        except Exception:
            pass
        return None

    async def set(
        self,
        key: str,
        value: Any,
        expiry_seconds: int = 300,
    ) -> bool:
        """
        Set a value in cache.

        Args:
            key: Cache key
            value: Value to cache (must be JSON serializable)
            expiry_seconds: TTL in seconds (default: 5 minutes)

        Returns:
            True if successful, False otherwise
        """
        if not self.is_connected or not self.redis_client:
            return False

        try:
            serialized = json.dumps(value)
            await self.redis_client.setex(key, expiry_seconds, serialized)
            return True
        except Exception:
            return False

    async def delete(self, key: str) -> bool:
        """
        Delete a value from cache.

        Args:
            key: Cache key

        Returns:
            True if deleted, False otherwise
        """
        if not self.is_connected or not self.redis_client:
            return False

        try:
            await self.redis_client.delete(key)
            return True
        except Exception:
            return False

    async def delete_pattern(self, pattern: str) -> int:
        """
        Delete all keys matching a pattern.

        Args:
            pattern: Redis key pattern (e.g., "weather:*")

        Returns:
            Number of keys deleted
        """
        if not self.is_connected or not self.redis_client:
            return 0

        try:
            keys = await self.redis_client.keys(pattern)
            if keys:
                return await self.redis_client.delete(*keys)
        except Exception:
            pass
        return 0

    async def clear_all(self) -> bool:
        """
        Clear all cached data.

        Returns:
            True if successful, False otherwise
        """
        if not self.is_connected or not self.redis_client:
            return False

        try:
            await self.redis_client.flushdb()
            return True
        except Exception:
            return False

    async def get_stats(self) -> dict:
        """
        Get cache statistics.

        Returns:
            Dictionary with cache statistics
        """
        if not self.is_connected or not self.redis_client:
            return {
                "connected": False,
                "message": "Redis not connected",
            }

        try:
            info = await self.redis_client.info()
            keys_count = len(await self.redis_client.keys("*"))
            return {
                "connected": True,
                "keys_count": keys_count,
                "used_memory_human": info.get("used_memory_human", "N/A"),
            }
        except Exception as e:
            return {
                "connected": False,
                "error": str(e),
            }


# Singleton instance
_cache_service: Optional[CacheService] = None


async def get_cache() -> CacheService:
    """
    Get or create cache service singleton instance.
    """

    global _cache_service
    if _cache_service is None:
        _cache_service = CacheService()
        await _cache_service.connect()
    return _cache_service


async def close_cache():
    """Close the cache service."""
    global _cache_service
    if _cache_service is not None:
        await _cache_service.disconnect()
        _cache_service = None
