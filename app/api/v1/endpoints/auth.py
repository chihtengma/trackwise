"""
Authentication endpoints.

This module handles user authentication including login and registration.
"""

from datetime import timedelta

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_async_db
from app.core.security import create_access_token
from app.schemas.user import UserCreate, UserResponse, Token
from app.services.user import UserService


router = APIRouter()


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_async_db)):
    """
    Register a new user.

    Creates a new user account with the provided information.

    Args:
        user_data: User registration information (email, username, password)
        db: Database session

    Returns:
        Newly created user information (without password)

    Raises:
        ResourceAlreadyExistsError: If email or username already exists

    Example Request:
        POST /api/v1/auth/register
        {
            "email": "john@example.com",
            "username": "john_doe",
            "password": "SecurePass123!",
            "full_name": "John Doe"
        }
    """
    # No try/except needed - exceptions handled by global handler
    user = await UserService.create_user(db, user_data)
    return user


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_async_db),
):
    """
    Login and get access token.

    Authenticates user with EMAIL and password,
    returns a JWT access token for subsequent requests.

    Note: Although the field is called 'username' (OAuth2 standard),
    we need to provide EMAIL address here.

    Args:
        form_data: OAuth2 password form (use email as username)
        db: Database session

    Returns:
        Access token and token type

    Raises:
        AuthenticationError: If credentials are invalid (401)
        InactiveUserError: If user account is inactive (403)

    Example Request:
        POST /api/v1/auth/login
        Content-Type: application/x-www-form-urlencoded

        username=john@example.com&password=SecurePass123!

        Note: Use your EMAIL in the 'username' field
    """
    # Authenticate user - exceptions handled by global handler
    user = await UserService.authenticate_user(
        db, form_data.username, form_data.password  # This is actually the email
    )

    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
