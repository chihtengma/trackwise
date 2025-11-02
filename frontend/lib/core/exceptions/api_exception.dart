/// Base exception for API errors
class ApiException implements Exception {
  final String message;
  final int? statusCode;
  final dynamic originalError;

  const ApiException({
    required this.message,
    this.statusCode,
    this.originalError,
  });

  @override
  String toString() => 'ApiException: $message (Status: $statusCode)';
}

/// Exception for network connectivity issues
class NetworkException extends ApiException {
  const NetworkException({
    super.message = 'No internet connection',
    super.statusCode,
    super.originalError,
  });
}

/// Exception for timeout errors
class TimeoutException extends ApiException {
  const TimeoutException({
    super.message = 'Request timeout',
    super.statusCode,
    super.originalError,
  });
}

/// Exception for authentication errors (401)
class UnauthorizedException extends ApiException {
  const UnauthorizedException({
    super.message = 'Authentication failed',
    super.statusCode = 401,
    super.originalError,
  });
}

/// Exception for forbidden errors (403)
class ForbiddenException extends ApiException {
  const ForbiddenException({
    super.message = 'Access forbidden',
    super.statusCode = 403,
    super.originalError,
  });
}

/// Exception for not found errors (404)
class NotFoundException extends ApiException {
  const NotFoundException({
    super.message = 'Resource not found',
    super.statusCode = 404,
    super.originalError,
  });
}

/// Exception for validation errors (422)
class ValidationException extends ApiException {
  final Map<String, dynamic>? errors;

  const ValidationException({
    super.message = 'Validation failed',
    super.statusCode = 422,
    super.originalError,
    this.errors,
  });
}

/// Exception for server errors (500+)
class ServerException extends ApiException {
  const ServerException({
    super.message = 'Server error',
    super.statusCode,
    super.originalError,
  });
}

/// Exception for unknown errors
class UnknownException extends ApiException {
  const UnknownException({
    super.message = 'An unknown error occurred',
    super.statusCode,
    super.originalError,
  });
}
