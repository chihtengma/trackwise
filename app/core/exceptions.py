"""
Custom exception classes for the application.

This module defines domain-specific exceptions that can be raised
in the service layer and converted to HTTP responses in the API layer.
"""

from fastapi import status


class AppException(Exception):
    """
    Base exception class for all application exceptions.

    All custom exceptions should inherit from this class.

    Attributes:
        status_code: Default HTTP status code for this exception type
        message: Human-readable error message
        details: Additional error details (dict)
    """

    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(self, message: str, details: dict | None = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class ResourceNotFoundError(AppException):
    """
    Raised when a requested resource is not found.

    HTTP Status: 404 Not Found

    Example:
        >>> raise ResourceNotFoundError("User not found", {"user_id": 123})
    """

    status_code = status.HTTP_404_NOT_FOUND


class ResourceAlreadyExistsError(AppException):
    """
    Raised when attempting to create a resource that already exists.

    HTTP Status: 409 Conflict

    Example:
        >>> raise ResourceAlreadyExistsError("Email already registered")
    """

    status_code = status.HTTP_409_CONFLICT


class AuthenticationError(AppException):
    """
    Raised when authentication fails.

    HTTP Status: 401 Unauthorized

    Example:
        >>> raise AuthenticationError("Invalid credentials")
    """

    status_code = status.HTTP_401_UNAUTHORIZED


class AuthorizationError(AppException):
    """
    Raised when user lacks permission for an action.

    HTTP Status: 403 Forbidden

    Example:
        >>> raise AuthorizationError("Insufficient privileges")
    """

    status_code = status.HTTP_403_FORBIDDEN


class ValidationError(AppException):
    """
    Raised when data validation fails.

    HTTP Status: 400 Bad Request

    Example:
        >>> raise ValidationError("Invalid email format")
    """

    status_code = status.HTTP_400_BAD_REQUEST


class InactiveUserError(AppException):
    """
    Raised when an inactive user attempts to perform an action.

    HTTP Status: 403 Forbidden

    Example:
        >>> raise InactiveUserError("User account is inactive")
    """

    status_code = status.HTTP_403_FORBIDDEN
