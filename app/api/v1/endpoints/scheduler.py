"""
Scheduler management endpoints.

This module provides endpoints for managing background tasks and scheduler.
"""

from typing import List, Dict

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_current_superuser
from app.core.scheduler import (
    get_jobs,
    pause_scheduler,
    resume_scheduler,
    is_scheduler_running,
)
from app.models.user import User

router = APIRouter()


@router.get("/jobs", response_model=List[Dict])
async def list_jobs(current_user: User = Depends(get_current_superuser)):
    """
    List all scheduled jobs.

    Returns information about all background tasks including their
    schedule and next run time.

    Args:
        current_user: Current authenticated superuser

    Returns:
        List of job information dictionaries

    Example Response:
        [
            {
                "id": "mta_refresh",
                "name": "MTA Data Refresh",
                "trigger": "interval[0:01:00]",
                "next_run_time": "2025-11-02T12:30:00Z"
            }
        ]
    """
    try:
        jobs = get_jobs()
        return jobs
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list jobs: {str(e)}",
        )


@router.get("/status", response_model=Dict)
async def get_scheduler_status(current_user: User = Depends(get_current_superuser)):
    """
    Get scheduler status.

    Returns whether the scheduler is running and basic stats.

    Args:
        current_user: Current authenticated superuser

    Returns:
        Scheduler status information

    Example Response:
        {
            "running": true,
            "jobs_count": 3
        }
    """
    try:
        is_running = is_scheduler_running()
        jobs = get_jobs()

        return {
            "running": is_running,
            "jobs_count": len(jobs),
            "jobs": jobs,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get scheduler status: {str(e)}",
        )


@router.post("/pause", response_model=Dict)
async def pause_scheduler_endpoint(current_user: User = Depends(get_current_superuser)):
    """
    Pause the scheduler.

    Temporarily stops all scheduled jobs. Jobs will not execute while paused.

    Args:
        current_user: Current authenticated superuser

    Returns:
        Success message

    Example Response:
        {
            "message": "Scheduler paused"
        }
    """
    try:
        pause_scheduler()
        return {"message": "Scheduler paused"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to pause scheduler: {str(e)}",
        )


@router.post("/resume", response_model=Dict)
async def resume_scheduler_endpoint(
    current_user: User = Depends(get_current_superuser),
):
    """
    Resume the scheduler.

    Resumes execution of scheduled jobs after being paused.

    Args:
        current_user: Current authenticated superuser

    Returns:
        Success message

    Example Response:
        {
            "message": "Scheduler resumed"
        }
    """
    try:
        resume_scheduler()
        return {"message": "Scheduler resumed"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to resume scheduler: {str(e)}",
        )
