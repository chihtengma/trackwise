import 'package:dio/dio.dart';

import '../../core/config/app_config.dart';
import '../../core/exceptions/api_exception.dart';
import '../models/user_model.dart';

/// Remote data source for authentication API calls
class AuthRemoteDataSource {
  final Dio dio;
  final AppConfig config;

  AuthRemoteDataSource({
    required this.dio,
    required this.config,
  });

  /// Register a new user
  Future<UserModel> register({
    required String email,
    required String username,
    required String password,
    String? fullName,
  }) async {
    try {
      final response = await dio.post(
        config.registerEndpoint,
        data: UserCreate(
          email: email,
          username: username,
          password: password,
          fullName: fullName,
        ).toJson(),
      );

      if (response.statusCode == 201) {
        return UserModel.fromJson(response.data);
      } else {
        throw UnknownException(message: 'Registration failed');
      }
    } on DioException catch (e) {
      throw _handleDioError(e);
    }
  }

  /// Login with email and password
  Future<TokenResponse> login({
    required String email,
    required String password,
  }) async {
    try {
      // OAuth2 form data format
      final response = await dio.post(
        config.loginEndpoint,
        data: {
          'username': email, // Backend uses email as username
          'password': password,
        },
        options: Options(
          headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        ),
      );

      if (response.statusCode == 200) {
        return TokenResponse.fromJson(response.data);
      } else {
        throw UnknownException(message: 'Login failed');
      }
    } on DioException catch (e) {
      throw _handleDioError(e);
    }
  }

  /// Login with social provider (Google/Apple)
  Future<TokenResponse> socialLogin({
    required String provider,
    required String idToken,
    String? accessToken,
    String? authorizationCode,
    String? nonce,
  }) async {
    try {
      final response = await dio.post(
        config.socialLoginEndpoint,
        data: {
          'provider': provider,
          'id_token': idToken,
          if (accessToken != null) 'access_token': accessToken,
          if (authorizationCode != null) 'authorization_code': authorizationCode,
          if (nonce != null) 'nonce': nonce,
        },
      );

      if (response.statusCode == 200) {
        return TokenResponse.fromJson(response.data);
      } else {
        throw UnknownException(message: 'Social login failed');
      }
    } on DioException catch (e) {
      throw _handleDioError(e);
    }
  }

  /// Handle Dio errors and convert to custom exceptions
  ApiException _handleDioError(DioException error) {
    if (error.type == DioExceptionType.connectionTimeout ||
        error.type == DioExceptionType.receiveTimeout ||
        error.type == DioExceptionType.sendTimeout) {
        return const TimeoutException(
          message: 'Request timeout',
        );
    }

    if (error.type == DioExceptionType.connectionError) {
      return const NetworkException();
    }

    final statusCode = error.response?.statusCode;

    if (statusCode != null && statusCode >= 500) {
      return const ServerException();
    }

    switch (statusCode) {
      case 401:
        return const UnauthorizedException();
      case 403:
        return const ForbiddenException();
      case 404:
        return const NotFoundException();
      case 422:
        return ValidationException(
          errors: error.response?.data,
        );
      default:
        return UnknownException(
          message: error.message ?? 'Unknown error',
          statusCode: statusCode,
        );
    }
  }
}
