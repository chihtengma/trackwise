"""
APScheduler configuration and management.

Provides centralized scheduler for background tasks like cache warming
and periodic data refreshes.
"""

from typing import Optional, Callable
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger

from app.core.config import settings

logger = logging.getLogger(__name__)


# Global scheduler instance
_scheduler: Optional[AsyncIOScheduler] = None


def get_scheduler() -> AsyncIOScheduler:
    """
    Get or create scheduler singleton instance.

    Returns:
        AsyncIOScheduler instance

    Example:
        >>> scheduler = get_scheduler()
        >>> scheduler.start()
    """
    global _scheduler
    if _scheduler is None:
        # Configure scheduler with timezone
        job_defaults = {
            "coalesce": True,  # Combine multiple pending jobs into one
            "max_instances": 3,  # Max concurrent instances of same job
        }
        _scheduler = AsyncIOScheduler(
            timezone="UTC",
            job_defaults=job_defaults,
        )
        logger.info("✅ APScheduler initialized")
    return _scheduler


async def start_scheduler():
    """
    Start the scheduler.

    Should be called during application startup.
    """
    if not settings.ENABLE_SCHEDULER:
        logger.info("⏭️  Scheduler disabled by configuration")
        return

    scheduler = get_scheduler()
    if not scheduler.running:
        scheduler.start()
        logger.info("🚀 APScheduler started")


async def stop_scheduler():
    """
    Stop the scheduler.

    Should be called during application shutdown.
    """
    global _scheduler
    if _scheduler is not None and _scheduler.running:
        _scheduler.shutdown(wait=True)
        _scheduler = None
        logger.info("🛑 APScheduler stopped")


def add_interval_job(
    func: Callable,
    interval_seconds: int,
    job_id: str,
    name: str,
    replace_existing: bool = True,
) -> bool:
    """
    Add a job that runs at specified intervals.

    Args:
        func: Async function to execute
        interval_seconds: Interval in seconds
        job_id: Unique job identifier
        name: Human-readable job name
        replace_existing: Whether to replace existing job with same ID

    Returns:
        True if job was added successfully

    Example:
        >>> async def refresh_data():
        ...     print("Refreshing data")
        >>> add_interval_job(refresh_data, 60, "refresh", "Data Refresh")
    """
    if not settings.ENABLE_SCHEDULER:
        return False

    try:
        scheduler = get_scheduler()
        trigger = IntervalTrigger(seconds=interval_seconds)
        scheduler.add_job(
            func=func,
            trigger=trigger,
            id=job_id,
            name=name,
            replace_existing=replace_existing,
        )
        logger.info(f"✅ Added interval job: {name} (every {interval_seconds}s)")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to add interval job {job_id}: {e}")
        return False


def add_cron_job(
    func: Callable,
    cron_expression: str,
    job_id: str,
    name: str,
    replace_existing: bool = True,
) -> bool:
    """
    Add a job that runs on a cron schedule.

    Args:
        func: Async function to execute
        cron_expression: Cron expression (e.g., "0 0 * * *" for daily at midnight)
        job_id: Unique job identifier
        name: Human-readable job name
        replace_existing: Whether to replace existing job with same ID

    Returns:
        True if job was added successfully

    Example:
        >>> async def daily_cleanup():
        ...     print("Daily cleanup")
        >>> add_cron_job(daily_cleanup, "0 0 * * *", "cleanup", "Daily Cleanup")
    """
    if not settings.ENABLE_SCHEDULER:
        return False

    try:
        scheduler = get_scheduler()
        # Parse cron expression: minute hour day month day_of_week
        parts = cron_expression.split()
        if len(parts) != 5:
            raise ValueError("Invalid cron expression: expected 5 parts")

        trigger = CronTrigger(
            minute=parts[0],
            hour=parts[1],
            day=parts[2],
            month=parts[3],
            day_of_week=parts[4],
        )
        scheduler.add_job(
            func=func,
            trigger=trigger,
            id=job_id,
            name=name,
            replace_existing=replace_existing,
        )
        logger.info(f"✅ Added cron job: {name} ({cron_expression})")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to add cron job {job_id}: {e}")
        return False


def remove_job(job_id: str) -> bool:
    """
    Remove a scheduled job.

    Args:
        job_id: Job identifier

    Returns:
        True if job was removed successfully
    """
    try:
        scheduler = get_scheduler()
        if scheduler.get_job(job_id):
            scheduler.remove_job(job_id)
            logger.info(f"✅ Removed job: {job_id}")
            return True
        return False
    except Exception as e:
        logger.error(f"❌ Failed to remove job {job_id}: {e}")
        return False


def get_jobs() -> list[dict]:
    """
    Get list of all scheduled jobs.

    Returns:
        List of job dictionaries with id, name, trigger, and next_run_time
    """
    scheduler = get_scheduler()
    jobs = []
    for job in scheduler.get_jobs():
        jobs.append(
            {
                "id": job.id,
                "name": job.name,
                "trigger": str(job.trigger),
                "next_run_time": (
                    job.next_run_time.isoformat() if job.next_run_time else None
                ),
            }
        )
    return jobs


def pause_scheduler():
    """Pause the scheduler temporarily."""
    if _scheduler and _scheduler.running:
        _scheduler.pause()
        logger.info("⏸️  Scheduler paused")


def resume_scheduler():
    """Resume the scheduler."""
    if _scheduler and _scheduler.running:
        _scheduler.resume()
        logger.info("▶️  Scheduler resumed")


def is_scheduler_running() -> bool:
    """Check if scheduler is running."""
    return _scheduler is not None and _scheduler.running
