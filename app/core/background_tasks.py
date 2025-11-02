"""
Background tasks for periodic operations.

This module defines tasks that run periodically, such as:
- MTA data refresh
- Cache warming
- Data cleanup
"""

import logging

from app.core.scheduler import add_interval_job
from app.core.config import settings
from app.services.mta_client import get_mta_client
from app.services.weather import WeatherService

logger = logging.getLogger(__name__)


async def mta_data_refresh():
    """
    Refresh MTA data for popular routes.

    This task runs periodically to keep transit data fresh in cache.
    """
    try:
        logger.info("🔄 Starting MTA data refresh")

        # Skip if MTA API key is not configured
        if not settings.MTA_API_KEY:
            logger.warning("⚠️  MTA API key not configured, skipping data refresh")
            logger.info("💡 Get your API key from: https://api.mta.info/")
            return

        client = get_mta_client()

        # Refresh data for popular routes
        popular_routes = ["A", "1", "2", "3", "4", "5", "6", "7", "N", "Q", "R", "W"]
        refreshed_count = 0

        for route_id in popular_routes:
            try:
                # Fetch trip updates to populate cache
                await client.get_trip_updates(route_id=route_id)
                refreshed_count += 1
            except Exception as e:
                logger.warning(f"Failed to refresh route {route_id}: {e}")

        logger.info(
            f"✅ MTA data refresh complete: "
            f"{refreshed_count}/{len(popular_routes)} routes"
        )
    except Exception as e:
        logger.error(f"❌ MTA data refresh failed: {e}")


async def cache_warm():
    """
    Warm up cache with popular queries.

    Pre-loads frequently requested data into cache to improve response times.
    """
    try:
        logger.info("🔥 Starting cache warming")

        # Warm weather cache for popular locations
        popular_locations = ["New York", "Brooklyn", "Queens", "Manhattan"]
        warmed_count = 0

        for location in popular_locations:
            try:
                await WeatherService.get_current_weather(location)
                warmed_count += 1
            except Exception as e:
                logger.warning(f"Failed to warm cache for {location}: {e}")

        logger.info(
            f"✅ Cache warming complete: "
            f"{warmed_count}/{len(popular_locations)} locations"
        )
    except Exception as e:
        logger.error(f"❌ Cache warming failed: {e}")


async def daily_cleanup():
    """
    Perform daily cleanup tasks.

    Can include:
    - Clean old cache entries
    - Archive old logs
    - Update statistics
    """
    try:
        logger.info("🧹 Starting daily cleanup")
        # Placeholder for cleanup tasks
        logger.info("✅ Daily cleanup complete")
    except Exception as e:
        logger.error(f"❌ Daily cleanup failed: {e}")


def register_scheduled_jobs():
    """
    Register all scheduled jobs with the scheduler.

    Should be called during application startup.
    """
    if not settings.ENABLE_SCHEDULER:
        logger.info("⏭️  Scheduler disabled, skipping job registration")
        return

    logger.info("📅 Registering scheduled jobs")

    # MTA data refresh - every 60 seconds by default
    add_interval_job(
        func=mta_data_refresh,
        interval_seconds=settings.MTA_REFRESH_INTERVAL_SECONDS,
        job_id="mta_refresh",
        name="MTA Data Refresh",
    )

    # Cache warming - every 5 minutes by default
    add_interval_job(
        func=cache_warm,
        interval_seconds=settings.CACHE_WARM_INTERVAL_MINUTES * 60,
        job_id="cache_warm",
        name="Cache Warming",
    )

    # Daily cleanup at midnight UTC
    from app.core.scheduler import add_cron_job

    add_cron_job(
        func=daily_cleanup,
        cron_expression="0 0 * * *",  # Daily at midnight UTC
        job_id="daily_cleanup",
        name="Daily Cleanup",
    )

    logger.info("✅ Scheduled jobs registered")
