import 'package:flutter_dotenv/flutter_dotenv.dart';

/// Application configuration loaded from environment variables
class AppConfig {
  // Singleton instance
  static final AppConfig _instance = AppConfig._internal();
  factory AppConfig() => _instance;
  AppConfig._internal();

  // Configuration getters
  String get baseUrl => dotenv.env['API_BASE_URL'] ?? 'http://localhost:8000';
  String get apiVersion => 'v1';
  String get appName => 'TrackWise';
  String get appVersion => '1.0.0';

  // API Endpoints
  String get apiBaseUrl => '$baseUrl/api/$apiVersion';
  
  // Auth endpoints
  String get loginEndpoint => '$apiBaseUrl/auth/login';
  String get registerEndpoint => '$apiBaseUrl/auth/register';
  
  // User endpoints
  String get userProfileEndpoint => '$apiBaseUrl/users/me';
  String get usersEndpoint => '$apiBaseUrl/users';
  
  // Saved routes endpoints
  String get savedRoutesEndpoint => '$apiBaseUrl/saved-routes';
  
  // Transit endpoints
  String get transitEndpoint => '$apiBaseUrl/transit';
  String transitRouteUpdatesEndpoint(String routeId) => 
      '$transitEndpoint/routes/$routeId/updates';
  String get transitQueryEndpoint => '$transitEndpoint/routes/query';
  
  // Weather endpoints
  String get weatherEndpoint => '$apiBaseUrl/weather';
  String get weatherCurrentEndpoint => '$weatherEndpoint/current';
  String get weatherQueryEndpoint => '$weatherEndpoint/query';

  /// Initialize configuration
  Future<void> initialize() async {
    await dotenv.load(fileName: '.env');
  }

  /// Get stored token (loaded from secure storage in actual implementation)
  String? get token => null; // Will be set by auth service
}
