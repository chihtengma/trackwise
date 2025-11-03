"""
User service - Business logic for user operations.

This module contains all business logic related to user management,
including CRUD operations and authentication helpers.
"""

from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash, verify_password
from app.core.exceptions import (
    ResourceNotFoundError,
    ResourceAlreadyExistsError,
    AuthenticationError,
    InactiveUserError,
)
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    """
    Service class for user-related operations.

    Handles all business logic for user management including
    creating, reading, updating, and deleting users.
    """

    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
        """
        Get a user by their ID.

        Args:
            db: Async database session
            user_id: The user's unique identifier

        Returns:
            User object if found, None otherwise

        Example:
            >>> user = await UserService.get_user_by_id(db, 1)
            >>> if user:
            ...     print(user.email)
        """
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
        """
        Get a user by their email address.

        Args:
            db: Async database session
            email: The user's email address

        Returns:
            User object if found, None otherwise

        Example:
            >>> user = await UserService.get_user_by_email(db, "john@example.com")
        """
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
        """
        Get a user by their username.

        Args:
            db: Async database session
            username: The user's username

        Returns:
            User object if found, None otherwise

        Example:
            >>> user = await UserService.get_user_by_username(db, "john_doe")
        """
        result = await db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_users(
        db: AsyncSession, skip: int = 0, limit: int = 100
    ) -> List[User]:
        """
        Get a list of users with pagination.

        Args:
            db: Async database session
            skip: Number of records to skip (for pagination)
            limit: Maximum number of records to return

        Returns:
            List of User objects

        Example:
            >>> users = await UserService.get_users(db, skip=0, limit=10)
            >>> for user in users:
            ...     print(user.username)
        """
        result = await db.execute(select(User).offset(skip).limit(limit))
        return list(result.scalars().all())

    @staticmethod
    async def create_user(db: AsyncSession, user_data: UserCreate) -> User:
        """
        Create a new user.

        Args:
            db: Async database session
            user_data: UserCreate schema with user information

        Returns:
            Newly created User object

        Raises:
            ResourceAlreadyExistsError: If email or username already exists

        Example:
            >>> user_data = UserCreate(
            ...     email="john@example.com",
            ...     username="john_doe",
            ...     password="SecurePass123!"
            ... )
            >>> user = await UserService.create_user(db, user_data)
        """
        # Check if email already exists
        existing_user = await UserService.get_user_by_email(db, user_data.email)
        if existing_user:
            raise ResourceAlreadyExistsError(
                "Email already registered", {"email": user_data.email}
            )

        # Check if username already exists
        existing_user = await UserService.get_user_by_username(db, user_data.username)
        if existing_user:
            raise ResourceAlreadyExistsError(
                "Username already taken", {"username": user_data.username}
            )

        # Hash the password
        hashed_password = get_password_hash(user_data.password)

        # Create user object
        db_user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password,
            full_name=user_data.full_name,
        )

        # Add to database
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)

        return db_user

    @staticmethod
    async def update_user(
        db: AsyncSession, user_id: int, user_data: UserUpdate
    ) -> User:
        """
        Update an existing user.

        Args:
            db: Async database session
            user_id: ID of the user to update
            user_data: UserUpdate schema with fields to update

        Returns:
            Updated User object

        Raises:
            ResourceNotFoundError: If user not found
            ResourceAlreadyExistsError: If new email/username is already taken

        Example:
            >>> update_data = UserUpdate(full_name="Jane Doe")
            >>> user = await UserService.update_user(db, 1, update_data)
        """
        # Get the user
        user = await UserService.get_user_by_id(db, user_id)
        if not user:
            raise ResourceNotFoundError("User not found", {"user_id": user_id})

        # Update fields if provided (exclude None values and unset fields)
        update_data = user_data.model_dump(exclude_unset=True, exclude_none=True)

        # Check email uniqueness if being updated
        if "email" in update_data and update_data["email"] != user.email:
            existing = await UserService.get_user_by_email(db, update_data["email"])
            if existing:
                raise ResourceAlreadyExistsError(
                    "Email already registered", {"email": update_data["email"]}
                )
            user.email = update_data["email"]

        # Check username uniqueness if being updated
        if "username" in update_data and update_data["username"] != user.username:
            existing = await UserService.get_user_by_username(
                db, update_data["username"]
            )
            if existing:
                raise ResourceAlreadyExistsError(
                    "Username already taken", {"username": update_data["username"]}
                )
            user.username = update_data["username"]

        # Update password if provided (and not None)
        if "password" in update_data and update_data["password"] is not None:
            user.hashed_password = get_password_hash(  # type: ignore[assignment]
                update_data["password"]
            )

        # Update profile picture if provided (allow None to clear it)
        if "profile_picture" in user_data.model_dump(exclude_unset=True):
            user.profile_picture = user_data.profile_picture

        # Update other fields
        if "full_name" in update_data:
            user.full_name = update_data["full_name"]
        if "is_active" in update_data:
            user.is_active = update_data["is_active"]

        await db.commit()
        await db.refresh(user)

        return user

    @staticmethod
    async def delete_user(db: AsyncSession, user_id: int) -> bool:
        """
        Delete a user.

        Args:
            db: Async database session
            user_id: ID of the user to delete

        Returns:
            True if deleted successfully

        Raises:
            ResourceNotFoundError: If user not found

        Example:
            >>> await UserService.delete_user(db, 1)
        """
        user = await UserService.get_user_by_id(db, user_id)
        if not user:
            raise ResourceNotFoundError("User not found", {"user_id": user_id})

        await db.delete(user)
        await db.commit()

        return True

    @staticmethod
    async def authenticate_user(db: AsyncSession, email: str, password: str) -> User:
        """
        Authenticate a user by email and password.

        Args:
            db: Async database session
            email: The user's email address
            password: The user's plain text password

        Returns:
            User object if authentication successful

        Raises:
            AuthenticationError: If authentication fails
            InactiveUserError: If user account is inactive

        Example:
            >>> user = await UserService.authenticate_user(
            ...     db,
            ...     "john@example.com",
            ...     "SecurePass123!"
            ... )
        """
        # Get user by email
        user = await UserService.get_user_by_email(db, email)

        # If user not found or password incorrect
        if not user or not verify_password(password, str(user.hashed_password)):
            raise AuthenticationError("Incorrect email or password")

        # Check if user is active
        if not user.is_active:
            raise InactiveUserError("User account is inactive")

        return user
