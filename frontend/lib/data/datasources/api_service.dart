import 'package:dio/dio.dart';

import '../../core/config/app_config.dart';
import '../../core/exceptions/api_exception.dart';
import '../models/saved_route_model.dart';
import '../models/transit_model.dart';
import '../models/user_model.dart';
import '../models/weather_model.dart';

/// Central API service for making backend calls
class ApiService {
  final Dio dio;
  final AppConfig config;

  ApiService({
    required this.dio,
    required this.config,
  });

  /// ===== USER ENDPOINTS =====

  /// Get current user profile
  Future<UserModel> getCurrentUser() async {
    try {
      final response = await dio.get(config.userProfileEndpoint);
      return UserModel.fromJson(response.data);
    } on DioException catch (e) {
      throw _handleDioError(e);
    }
  }

  /// Update user profile
  Future<UserModel> updateUser(int userId, UserUpdate updates) async {
    try {
      final response = await dio.patch(
        '${config.usersEndpoint}/$userId',
        data: updates.toJson(),
      );
      return UserModel.fromJson(response.data);
    } on DioException catch (e) {
      throw _handleDioError(e);
    }
  }

  /// ===== SAVED ROUTES ENDPOINTS =====

  /// Get all saved routes for current user
  Future<SavedRouteListResponse> getSavedRoutes({
    int skip = 0,
    int limit = 100,
    bool favoritesOnly = false,
  }) async {
    try {
      final response = await dio.get(
        config.savedRoutesEndpoint,
        queryParameters: {
          'skip': skip,
          'limit': limit,
          'favorites_only': favoritesOnly,
        },
      );
      return SavedRouteListResponse.fromJson(response.data);
    } on DioException catch (e) {
      throw _handleDioError(e);
    }
  }

  /// Get a specific saved route
  Future<SavedRouteModel> getSavedRoute(int routeId) async {
    try {
      final response = await dio.get('${config.savedRoutesEndpoint}/$routeId');
      return SavedRouteModel.fromJson(response.data);
    } on DioException catch (e) {
      throw _handleDioError(e);
    }
  }

  /// Create a new saved route
  Future<SavedRouteModel> createSavedRoute(SavedRouteCreate route) async {
    try {
      final response = await dio.post(
        config.savedRoutesEndpoint,
        data: route.toJson(),
      );
      return SavedRouteModel.fromJson(response.data);
    } on DioException catch (e) {
      throw _handleDioError(e);
    }
  }

  /// Update a saved route
  Future<SavedRouteModel> updateSavedRoute(
    int routeId,
    SavedRouteUpdate updates,
  ) async {
    try {
      final response = await dio.put(
        '${config.savedRoutesEndpoint}/$routeId',
        data: updates.toJson(),
      );
      return SavedRouteModel.fromJson(response.data);
    } on DioException catch (e) {
      throw _handleDioError(e);
    }
  }

  /// Delete a saved route
  Future<void> deleteSavedRoute(int routeId) async {
    try {
      await dio.delete('${config.savedRoutesEndpoint}/$routeId');
    } on DioException catch (e) {
      throw _handleDioError(e);
    }
  }

  /// ===== TRANSIT ENDPOINTS =====

  /// Get real-time trip updates for a route
  Future<List<TripUpdate>> getRouteUpdates(String routeId) async {
    try {
      final response = await dio.get(
        config.transitRouteUpdatesEndpoint(routeId),
      );
      return (response.data as List)
          .map((json) => TripUpdate.fromJson(json))
          .toList();
    } on DioException catch (e) {
      throw _handleDioError(e);
    }
  }

  /// Query routes from origin to destination
  Future<RouteResponse> queryRoutes(RouteQuery query) async {
    try {
      final response = await dio.post(
        config.transitQueryEndpoint,
        data: query.toJson(),
      );
      return RouteResponse.fromJson(response.data);
    } on DioException catch (e) {
      throw _handleDioError(e);
    }
  }

  /// ===== WEATHER ENDPOINTS =====

  /// Get current weather for a location
  Future<WeatherCurrentResponse> getCurrentWeather({
    required String location,
    String units = 'metric',
  }) async {
    try {
      final response = await dio.get(
        config.weatherCurrentEndpoint,
        queryParameters: {
          'location': location,
          'units': units,
        },
      );
      return WeatherCurrentResponse.fromJson(response.data);
    } on DioException catch (e) {
      throw _handleDioError(e);
    }
  }

  /// Query weather (POST alternative)
  Future<WeatherCurrentResponse> queryWeather({
    required String location,
    String units = 'metric',
  }) async {
    try {
      final response = await dio.post(
        config.weatherQueryEndpoint,
        data: WeatherQuery(location: location).toJson(),
        queryParameters: {'units': units},
      );
      return WeatherCurrentResponse.fromJson(response.data);
    } on DioException catch (e) {
      throw _handleDioError(e);
    }
  }

  /// Handle Dio errors and convert to custom exceptions
  ApiException _handleDioError(DioException error) {
    if (error.type == DioExceptionType.connectionTimeout ||
        error.type == DioExceptionType.receiveTimeout ||
        error.type == DioExceptionType.sendTimeout) {
      return const TimeoutException();
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
