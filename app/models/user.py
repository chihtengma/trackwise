"""
User model for authentication and user management.

This module defines the User table and related database operations.
"""

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func

from app.core.database import Base


class User(Base):
    """
    User model for storing user account information.

    Attributes:
        id: Primary key, auto-incrementing integer
        email: Unique email address for login
        username: Unique username for display
        hashed_password: Argon2 hashed password
        full_name: User's full name (optional)
        is_active: Whether the account is active
        is_superuser: Whether the user has admin privileges
        preferences: JSON filed for user preferences (route preferences, theme, etc.)
        created)at: Timestamp when the account was created
        updated_at: Timestamp when the account was last updated

    Example:
        >>> user = User(
        ...     email="user@example.com",
        ...     username="john_doe",
        ...     hashed_password=argon2.hash("password123"),
        ...    full_name="John Doe"
            )
        >>> db.add(user)
        >>> db.commit()
    """

    # Table name
    __tablename__ = "users"

    # Primary key
    id = Column(
        Integer,  # Auto-incrementing integer
        primary_key=True,  # Primary key
        index=True,  # Index for faster lookups
        comment="Unique user identifier",  # Comment for the column
    )

    # Authentication Fields
    email = Column(
        String(50),  # Email address (max 50 characters)
        unique=True,
        index=True,
        nullable=False,
        comment="User's email address (unique, used for login)",
    )
    username = Column(
        String(50),
        unique=True,
        index=True,
        nullable=False,
        comment="User's username (unique, used for display)",
    )
    hashed_password = Column(
        String(255), nullable=False, comment="Argon2 hashed password"
    )

    # Status Fields
    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
        comment="Whether the user account is active",
    )
    is_superuser = Column(
        Boolean,
        default=False,
        nullable=False,
        comment="Whether the user has admin privileges",
    )

    # User Preferences
    preferences = Column(
        Text,
        nullable=True,
        comment=(
            "JSON string for user preferences"
            "(favorite routes, notification preferences, theme, etc.)"
        ),
    )

    # Timestamps
    created_at = Column(
        DateTime(timezone=True),  # Timestamp with timezone
        server_default=func.now(),  # Set default to current timestamp
        nullable=False,
        comment="Timestamp when the user was created",
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        comment="Timestamp when the user was last updated",
    )

    def __repr__(self) -> str:
        """
        String representation of the User object.

        Returns:
            String representation showing key user information

        Example: <User(id=1, username='john_doe', email='user@example.com')>
        """
        return (
            f"<User(id={self.id}, username='{self.username}', "
            f"email='{self.email}')>"
        )

    def to_dict(self) -> dict:
        """
        Convert User object to dictionary.

        Returns:
            Dictionary representation of the user (excludes sensitive data)

        Example:
            >>> user = User(id=1, email='user@example.com', username='john_doe')
            >>> user.to_dict()
            {'id': 1, 'email': 'user@example.com', 'username': 'john_doe'}
        """
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "full_name": self.full_name,
            "is_active": self.is_active,
            "is_superuser": self.is_superuser,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
