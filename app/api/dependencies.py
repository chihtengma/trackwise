"""
API dependencies for FastAPI endpoints.

This module provides reusable dependencies for authentication,
database sessions, and other common requirements.
"""

from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_db
from app.core.security import decode_access_token
from app.models import User
from app.services.user import UserService


# OAuth2 scheme for token authentication
# tokenUrl is the endpoint where users can get tokens
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_async_db)
) -> User:
    """
    Dependency to get the current authenticated user from JWT token.

    This dependency:
    1. Extracts the JWT token from the Authorization header
    2. Decodes and validates the token
    3. Retrieves the user from the database by email
    4. Returns the user object

    Args:
        token: JWT access token from Authorization header
        db: Database session

    Returns:
        Current authenticated User object

    Raises:
        HTTPException: If token is invalid or user not found

    Example:
        >>> @app.get("/protected")
        >>> async def protected_route(user: User = Depends(get_current_user)):
        ...     return {"message": f"Hello {user.username}"}
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Decode the token
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    # Extract email from token (stored as 'sub')
    email: Optional[str] = payload.get("sub")
    if email is None:
        raise credentials_exception

    # Get user from database by email
    user = await UserService.get_user_by_email(db, email)
    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Dependency to get the current active user.

    Args:
        current_user: Current authenticated user

    Returns:
        Active User object

    Raises:
        HTTPException: If user account is inactive

    Example:
        >>> @app.get("/active-only")
        >>> async def active_route(user: User = Depends(get_current_active_user)):
        ...     return {"message": "You're active!"}
    """

    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )
    return current_user


async def get_current_superuser(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """
    Dependecny to get the current superuser.
    Ensures the authenticated user has admin privileges.

    Args:
        current_user: Current active authenticated user

    Returns:
        Superuser User object

    Raises:
        HTTPException: If user is not a superuser

    Example:
        >>> @app.delete("/admin/users/{user_id}")
        >>> async def delete_user(
        ...     user_id: int,
        ...     admin: User = Depends(get_current_superuser)
        ... ):
        ...     # Only admins can access this
        ...     pass
    """

    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The operation requires superuser privileges",
        )
    return current_user
