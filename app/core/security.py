"""
Security utilities for authentication and password hashing.

This module provides functions for:
- Password hashing and verification (Argon2)
- JWT token creation and decoding
"""

from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any

from jose import JWTError, jwt
from pwdlib import PasswordHash
from pwdlib.hashers import argon2

from app.core.config import settings

# Initialize password hasher with Argon2
# Argon2 is considered the most secure password hashing algorithm
password_context = PasswordHash([argon2.Argon2Hasher()])


def get_password_hash(password: str) -> str:
    """
    Hash a plain text password using Argon2.

    Args:
        password: Plain text password to hash

    Returns:
        Hashed password string

    Example:
        >>> hashed = get_password_hash("my_password")
        >>> len(hashed) > 50  # Argon2 produces long hashes
        True
    """
    return password_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain text password against a hashed password.

    Args:
        plain_password: Plain text password to verify
        hashed_password: Previously hashed password from database

    Returns:
        True if password matches, False otherwise

    Example:
        >>> hashed = get_password_hash("secret")
        >>> verify_password("secret", hashed)
        True
        >>> verify_password("wrong", hashed)
        False
    """
    return password_context.verify(plain_password, hashed_password)


def create_access_token(
    data: Dict[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a JWT access token.

    Args:
        data: Dictionary of data to encode in the token (typically {"sub": user_email})
        expires_delta: Optional expiration time delta. If not provided,
                      uses ACCESS_TOKEN_EXPIRE_MINUTES from settings

    Returns:
        Encoded JWT token string

    Example:
        >>> token = create_access_token(data={"sub": "user@example.com"})
        >>> len(token) > 50  # JWT tokens are long strings
        True
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    # Add expiration time to token data
    to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc)})

    # Encode the token using HS256 algorithm
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    return encoded_jwt


def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Decode and verify a JWT access token.

    Args:
        token: JWT token string to decode

    Returns:
        Decoded token payload (dict) if valid, None if invalid/expired

    Raises:
        JWTError: If token is malformed or invalid

    Example:
        >>> token = create_access_token(data={"sub": "user@example.com"})
        >>> payload = decode_access_token(token)
        >>> payload["sub"]
        'user@example.com'
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        # Token is invalid, expired, or malformed
        return None
