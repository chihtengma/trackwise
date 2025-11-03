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
from app.schemas.user import UserCreate, UserResponse, Token, SocialLoginRequest, SocialAuthResponse
from app.services.user import UserService
from app.services.social_auth import SocialAuthService
from app.core.exceptions import AuthenticationError


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


@router.post("/social/login", response_model=SocialAuthResponse)
async def social_login(
    social_data: SocialLoginRequest,
    db: AsyncSession = Depends(get_async_db),
):
    """
    Authenticate via social provider (Google or Apple).

    Verifies the token with the provider and creates/updates user account.

    Args:
        social_data: Social login data including provider and tokens
        db: Database session

    Returns:
        Access token and user information

    Raises:
        AuthenticationError: If token verification fails (401)

    Example Request:
        POST /api/v1/auth/social/login
        {
            "provider": "google",
            "id_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
            "access_token": "ya29.a0AfH6SMBx..."
        }
    """
    # Authenticate with social provider
    result = await SocialAuthService.authenticate_social_user(
        db,
        provider=social_data.provider,
        token=social_data.id_token,
        authorization_code=social_data.authorization_code,
        nonce=social_data.nonce,
    )

    if not result:
        raise AuthenticationError("Invalid social authentication token")

    # Check if this is a new user
    is_new_user = result.get("user", {}).get("created_at") == result.get("user", {}).get("updated_at")

    return {
        "access_token": result["access_token"],
        "token_type": result["token_type"],
        "user": result["user"],
        "is_new_user": is_new_user,
    }


@router.post("/social/google", response_model=SocialAuthResponse)
async def google_login(
    id_token: str,
    access_token: str = None,
    db: AsyncSession = Depends(get_async_db),
):
    """
    Authenticate via Google Sign-In.

    Simplified endpoint specifically for Google authentication.

    Args:
        id_token: Google ID token
        access_token: Google access token (optional)
        db: Database session

    Returns:
        Access token and user information

    Example Request:
        POST /api/v1/auth/social/google
        {
            "id_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
            "access_token": "ya29.a0AfH6SMBx..."
        }
    """
    return await social_login(
        SocialLoginRequest(
            provider="google",
            id_token=id_token,
            access_token=access_token,
        ),
        db,
    )


@router.post("/social/apple", response_model=SocialAuthResponse)
async def apple_login(
    id_token: str,
    authorization_code: str = None,
    nonce: str = None,
    db: AsyncSession = Depends(get_async_db),
):
    """
    Authenticate via Apple Sign-In.

    Simplified endpoint specifically for Apple authentication.

    Args:
        id_token: Apple ID token
        authorization_code: Apple authorization code (optional)
        nonce: Nonce for verification (optional)
        db: Database session

    Returns:
        Access token and user information

    Example Request:
        POST /api/v1/auth/social/apple
        {
            "id_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
            "authorization_code": "c1234...",
            "nonce": "random_nonce_string"
        }
    """
    return await social_login(
        SocialLoginRequest(
            provider="apple",
            id_token=id_token,
            authorization_code=authorization_code,
            nonce=nonce,
        ),
        db,
    )
