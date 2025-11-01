"""
User management endpoints.

This module handles user CRUD operations (Create, Read, Update, Delete).
"""

from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_active_user, get_current_superuser
from app.core.database import get_async_db
from app.core.exceptions import AuthorizationError
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate
from app.services.user import UserService


router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def read_current_user(current_user: User = Depends(get_current_active_user)):
    """
    Get current user information.

    Returns information about the currently authenticated user.

    Args:
        current_user: Current authenticated user

    Returns:
        Current user information

    Example Request:
        GET /api/v1/users/me
        Authorization: Bearer <token>
    """
    return current_user


@router.get("/{user_id}", response_model=UserResponse)
async def read_user(
    user_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Get user by ID.

    Retrieve information about a specific user.
    Regular users can only view their own profile.
    Superusers can view any user's profile.

    Args:
        user_id: ID of the user to retrieve
        db: Database session
        current_user: Current authenticated user

    Returns:
        User information

    Raises:
        AuthorizationError: If user tries to access another user's profile (403)
        ResourceNotFoundError: If user not found (404)
    """
    # Check permission: users can only see their own profile unless superuser
    if user_id != current_user.id and not current_user.is_superuser:
        raise AuthorizationError(
            "User does not have permission to access this profile",
            {"user_id": user_id, "current_user_id": current_user.id},
        )

    # Service will raise ResourceNotFoundError if not found
    user = await UserService.get_user_by_id(db, user_id)
    if not user:
        from app.core.exceptions import ResourceNotFoundError

        raise ResourceNotFoundError("User not found", {"user_id": user_id})

    return user


@router.get("/", response_model=List[UserResponse])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_superuser),
):
    """
    Get list of users (Admin only).

    Retrieve a paginated list of all users.
    Only accessible by superusers.

    Args:
        skip: Number of records to skip (pagination)
        limit: Maximum number of records to return
        db: Database session
        current_user: Current authenticated superuser

    Returns:
        List of users
    """
    users = await UserService.get_users(db, skip=skip, limit=limit)
    return users


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Partially update user information (PATCH).

    Only updates the fields provided in the request.
    Regular users can only update their own profile.
    Superusers can update any user's profile.

    Args:
        user_id: ID of the user to update
        user_data: Updated user information
        db: Database session
        current_user: Current authenticated user

    Returns:
        Updated user information

    Raises:
        AuthorizationError: If user tries to update another user's profile (403)
        ResourceNotFoundError: If user not found (404)
        ResourceAlreadyExistsError: If email/username already taken (409)
    """
    # Check permission
    if user_id != current_user.id and not current_user.is_superuser:
        raise AuthorizationError(
            "User does not have permission to update this profile",
            {"user_id": user_id, "current_user_id": current_user.id},
        )

    # Service handles all validation and raises appropriate exceptions
    user = await UserService.update_user(db, user_id, user_data)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_superuser),
):
    """
    Delete a user (Admin only).

    Permanently delete a user account.
    Only accessible by superusers.

    Args:
        user_id: ID of the user to delete
        db: Database session
        current_user: Current authenticated superuser

    Raises:
        ResourceNotFoundError: If user not found (404)
    """
    # Service handles validation and raises ResourceNotFoundError if needed
    await UserService.delete_user(db, user_id)
