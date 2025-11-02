import '../../data/models/user_model.dart';

/// Interface for authentication repository
abstract class AuthRepository {
  /// Register a new user
  Future<UserModel> register({
    required String email,
    required String username,
    required String password,
    String? fullName,
  });

  /// Login with email and password
  Future<bool> login({
    required String email,
    required String password,
  });

  /// Logout and clear authentication data
  Future<void> logout();

  /// Check if user is authenticated
  Future<bool> isAuthenticated();

  /// Get current access token
  Future<String?> getAccessToken();
}
