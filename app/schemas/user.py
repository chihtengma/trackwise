"""
User schemas for request/response validation.

This module defines Pydantic models for user-realted data validation.
serialization, and API documentation.
"""

import re

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator

# ==================== Base Schemas ====================


class UserBase(BaseModel):
    """
    Base user schema with common fields.

    This is the base class that other user schemas inherit from.
    Contains fields that are common across ddifferent user operations.
    """

    email: EmailStr = Field(
        ...,
        description="User's email address",
        example="user@example.com",
    )
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="User's username",
        example="john_doe",
    )
    full_name: Optional[str] = Field(
        None,
        max_length=255,
        description="User's full name",
        example="[John Doe]",
    )

    @field_validator("username")
    @classmethod
    def username_alphanumeric(cls, val: str) -> str:
        """
        Validate that username contains only
        alphanumeric characters and underscores.

        Args:
            val: The username to validate.

        Returns:
            The validated username.

        Raises:
            ValueError: If username contains invalid characters. Got: '{val}'
        """
        import re

        # Regex pattern: at least one letter, only alphanumeric or underscores
        if not re.match(r"^(?=.*[A-Za-z])\w+$", val):
            raise ValueError(
                f"Username must contain at least one letter, and only "
                f"alphanumeric characters or underscores. Got: '{val}'"
            )
        return val


# ==================== Request Schemas ====================


class UserCreate(UserBase):
    """
    Schema for creating a new user.

    Used in user registration endpoints.
    Includes password field which won't be stored directly in the database.

    Example:
        >>> user_date = UserCreate(
        ...     email="user@example.com",
        ...     username="john_doe",
        ...     full_name="John Doe",
        ...     password="password123",
        ... )
    """

    password: str = Field(
        ...,
        min_length=8,
        max_length=100,
        description="User's password (will be hashed before storage)",
        examples=["password123", "securePassword!1"],
    )

    @field_validator("password")
    @classmethod
    def password_strength(cls, val: str) -> str:
        """
        Validate password strength using regex patterns.

        Ensures password meets minimum security requirements:
        - At least 8 characters
        - Contains at least one uppercase letter
        - Contains at least one lowercase letter
        - Contains at least one number
        - Contains at least one special character

        Args:
            val: The password to validate.

        Returns:
            The validated password.

        Raises:
            ValueError: If password doesn't meet requirements,
        """
        if len(val) < 8:
            raise ValueError("Password must be at least 8 characters long.")

        if not re.search(r"[A-Z]", val):
            raise ValueError("Password must contain at least one uppercase letter.")

        if not re.search(r"[a-z]", val):
            raise ValueError("Password must contain at least one lowercase letter.")

        if not re.search(r"\d", val):
            raise ValueError("Password must contain at least one number.")

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", val):
            raise ValueError("Password must contain at least one special character.")

        return val


class UserUpdate(UserBase):
    """
    Schema for updating user information.

    All fields are optional since users may update only specific fields.

    Example:
        >>> update_data = UserUpdate(full_name="Jane Doe")
    """

    email: Optional[EmailStr] = Field(None, description="New email address")
    username: Optional[str] = Field(
        None, min_length=3, max_length=50, description="New username"
    )
    full_name: Optional[str] = Field(
        None, max_length=255, description="Update full name"
    )
    password: Optional[str] = Field(
        None, min_length=8, max_length=100, description="New password"
    )
    is_active: Optional[bool] = Field(None, description="Account active status")


# ==================== Response Schemas ====================


class UserResponse(UserBase):
    """
    Schema for user response.

    Used when returning user data from API endpoints.
    Excludes sensitive fields like hashed password.

    Example:
        >>> user = UserResponse(
        ...     id=1,
        ...     email="john@example.com",
        ...     username="john_doe",
        ...     full_name="John Doe",
        ...     is_active=True,
        ...     is_superuser=False,
        ...     created_at=datetime.now(),
        ...     updated_at=datetime.now()
        ... )
    """

    id: int = Field(..., description="Unique user identifier")
    is_active: bool = Field(..., description="Account active status")
    is_superuser: bool = Field(..., description="Admin privileges status")
    created_at: datetime = Field(..., description="Timestamp when the user was created")
    updated_at: datetime = Field(
        ..., description="Timestamp when the user was last updated"
    )

    # Pydantic configuration
    model_confiog = {
        "from_attributes": True,  # Allows creation from ORM models
        "json_schema_extra": {
            "example": {
                "id": 1,
                "email": "john@example.com",
                "username": "john_doe",
                "full_name": "John Doe",
                "is_active": True,
                "is_superuser": False,
                "created_at": "2025-10-31T12:00:00Z",
                "updated_at": "2025-10-31T12:00:00Z",
            }
        },
    }


class UserInDB(UserResponse):
    """
    Schema for user data as stored in the database.

    Includes hased_password field. Should never be returned to client.
    Used internally for authentication operations.
    """

    hashed_password: str = Field(..., description="Argon2 hashed password")


# ==================== Authentication Schemas ====================


class Token(BaseModel):
    """
    Schema for JWT token response.

    Returned after successful login/authentication.

    Example:
        >>> token = Token(
        ...     access_token="your_access_token",
        ...     token_type="bearer",
        )
    """

    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(
        default="bearer", description="Token type (always 'bearer')"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
            }
        }
    }


class TokenData(BaseModel):
    """
    Schema for token payload data.

    Represents the deta decoded from a JWT token.
    Used internally forr authentication.

    Example:
        >>> token_data = TokenData(username="john_doe")
    """

    username: Optional[str] = Field(None, description="Username from token")
