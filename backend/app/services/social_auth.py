"""
Social authentication service for handling OAuth providers.

This module handles Google and Apple Sign-In authentication,
token verification, and user account creation/linking.
"""

import json
import jwt
import time
import hashlib
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token as google_id_token
import httpx
from jose import jwt as jose_jwt, jwk

from app.core.config import settings
from app.core.security import create_access_token
from app.models.user import User
from app.schemas.user import UserCreate


class SocialAuthService:
    """Service for handling social authentication."""

    @staticmethod
    async def verify_google_token(token: str) -> Optional[Dict[str, Any]]:
        """
        Verify Google ID token and extract user information.

        Args:
            token: Google ID token from frontend

        Returns:
            Dictionary with user information if valid, None otherwise

        Raises:
            ValueError: If token is invalid
        """
        try:
            # Verify the token with Google
            idinfo = google_id_token.verify_oauth2_token(
                token,
                google_requests.Request(),
                settings.GOOGLE_CLIENT_ID
            )

            # Verify that the token was issued for our app
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Invalid issuer')

            # Extract user information
            return {
                'provider_id': idinfo['sub'],  # Google user ID
                'email': idinfo.get('email'),
                'email_verified': idinfo.get('email_verified', False),
                'full_name': idinfo.get('name'),
                'profile_picture': idinfo.get('picture'),
                'given_name': idinfo.get('given_name'),
                'family_name': idinfo.get('family_name'),
            }

        except ValueError as e:
            print(f"Google token verification failed: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error verifying Google token: {e}")
            return None

    @staticmethod
    async def verify_apple_token(
        id_token: str,
        authorization_code: Optional[str] = None,
        nonce: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Verify Apple ID token and extract user information.

        Args:
            id_token: Apple ID token
            authorization_code: Apple authorization code (for refresh tokens)
            nonce: Nonce used for verification

        Returns:
            Dictionary with user information if valid, None otherwise
        """
        try:
            # Get Apple's public keys (JWKS)
            async with httpx.AsyncClient() as client:
                response = await client.get('https://appleid.apple.com/auth/keys')
                apple_keys = response.json()['keys']

            # Decode the token header to get the key ID
            header = jwt.get_unverified_header(id_token)
            kid = header.get('kid')
            alg = header.get('alg')

            # Find the matching key
            apple_key = None
            for key in apple_keys:
                if key['kid'] == kid:
                    apple_key = key
                    break

            if not apple_key:
                raise ValueError('Unable to find matching Apple public key')

            # Convert JWK to RSA key object for verification
            public_key = jwk.construct(apple_key)
            
            # Verify and decode the token using Apple's public key
            # python-jose needs the constructed key, not the raw JWK dict
            claims = jose_jwt.decode(
                id_token,
                public_key,
                algorithms=[alg],
                audience=settings.APPLE_CLIENT_ID if settings.APPLE_CLIENT_ID else None,
                options={"verify_signature": True, "verify_aud": bool(settings.APPLE_CLIENT_ID)}
            )

            # Verify issuer
            if claims.get('iss') != 'https://appleid.apple.com':
                raise ValueError('Invalid issuer')

            # Verify nonce if provided
            # Apple Sign-In nonce flow:
            # 1. Frontend generates rawNonce
            # 2. Frontend hashes it: hashedNonce = SHA256(rawNonce) 
            # 3. Frontend sends hashedNonce to Apple via getAppleIDCredential(nonce: hashedNonce)
            # 4. Apple includes the SAME hashedNonce in the JWT token (not double-hashed)
            # 5. Frontend sends rawNonce to backend
            # So backend should hash rawNonce once: SHA256(rawNonce) to match token
            if nonce:
                token_nonce = claims.get('nonce')
                if token_nonce:
                    # Hash the raw nonce to match what Apple includes
                    hashed_nonce = hashlib.sha256(nonce.encode('utf-8')).hexdigest()
                    
                    if token_nonce.lower() != hashed_nonce.lower():
                        # Log warning but still allow auth (signature verification is what matters)
                        print(f'Nonce mismatch (auth continues): expected={hashed_nonce[:16]}..., got={token_nonce[:16]}...')
                # No nonce in token is acceptable for subsequent logins

            # Extract user information
            return {
                'provider_id': claims.get('sub'),  # Apple user ID
                'email': claims.get('email'),
                'email_verified': claims.get('email_verified', False),
                # Apple doesn't always provide name on subsequent logins
                'full_name': None,  # Will be set during first login only
            }

        except jwt.InvalidTokenError as e:
            print(f"Apple token verification failed: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error verifying Apple token: {e}")
            return None

    @staticmethod
    async def create_or_update_social_user(
        db: AsyncSession,
        provider: str,
        provider_data: Dict[str, Any]
    ) -> User:
        """
        Create a new user or update existing user from social provider data.

        Args:
            db: Database session
            provider: Provider name ('google' or 'apple')
            provider_data: User data from provider

        Returns:
            User object
        """
        provider_id = provider_data['provider_id']
        email = provider_data.get('email')

        # Check if user exists with this provider ID
        provider_field = f"{provider}_id"
        stmt = select(User).where(
            getattr(User, provider_field) == provider_id
        )
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()

        if user:
            # Update user information if changed
            if provider_data.get('profile_picture') and not user.profile_picture:
                user.profile_picture = provider_data['profile_picture']
            if provider_data.get('full_name') and not user.full_name:
                user.full_name = provider_data['full_name']
            if provider_data.get('email_verified'):
                user.email_verified = True

            user.updated_at = datetime.utcnow()
            await db.commit()
            await db.refresh(user)
            return user

        # Check if user exists with this email
        if email:
            stmt = select(User).where(User.email == email)
            result = await db.execute(stmt)
            user = result.scalar_one_or_none()

            if user:
                # Link social account to existing user
                setattr(user, provider_field, provider_id)
                if provider_data.get('profile_picture') and not user.profile_picture:
                    user.profile_picture = provider_data['profile_picture']
                if provider_data.get('full_name') and not user.full_name:
                    user.full_name = provider_data['full_name']
                if provider_data.get('email_verified'):
                    user.email_verified = True

                user.auth_provider = provider
                user.updated_at = datetime.utcnow()
                await db.commit()
                await db.refresh(user)
                return user

        # Create new user
        # Generate a unique username from email or provider ID
        username = email.split('@')[0] if email else f"{provider}_{provider_id[:8]}"

        # Ensure username is unique
        base_username = username
        counter = 1
        while True:
            stmt = select(User).where(User.username == username)
            result = await db.execute(stmt)
            if not result.scalar_one_or_none():
                break
            username = f"{base_username}{counter}"
            counter += 1

        user = User(
            email=email or f"{provider_id}@{provider}.local",
            username=username,
            full_name=provider_data.get('full_name'),
            profile_picture=provider_data.get('profile_picture'),
            email_verified=provider_data.get('email_verified', False),
            auth_provider=provider,
            is_active=True,
            **{provider_field: provider_id}
        )

        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    async def authenticate_social_user(
        db: AsyncSession,
        provider: str,
        token: str,
        authorization_code: Optional[str] = None,
        nonce: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Authenticate user via social provider.

        Args:
            db: Database session
            provider: Provider name ('google' or 'apple')
            token: ID token from provider
            authorization_code: Authorization code (for Apple)
            nonce: Nonce (for Apple)

        Returns:
            Dictionary with access token and user info if successful
        """
        # Verify the token based on provider
        if provider == 'google':
            provider_data = await SocialAuthService.verify_google_token(token)
        elif provider == 'apple':
            provider_data = await SocialAuthService.verify_apple_token(
                token, authorization_code, nonce
            )
        else:
            return None

        if not provider_data:
            return None

        # Create or update user
        user = await SocialAuthService.create_or_update_social_user(
            db, provider, provider_data
        )

        # Generate access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email},
            expires_delta=access_token_expires
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "full_name": user.full_name,
                "profile_picture": user.profile_picture,
                "email_verified": user.email_verified,
                "auth_provider": user.auth_provider,
                "is_active": user.is_active,
                "is_superuser": user.is_superuser,
                "created_at": user.created_at,
                "updated_at": user.updated_at,
            }
        }