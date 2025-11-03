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

  /// Login with social provider (Google/Apple)
  Future<bool> socialLogin({
    required String provider,
    required String idToken,
    String? accessToken,
    String? authorizationCode,
    String? nonce,
  });

  /// Logout and clear authentication data
  Future<void> logout();

  /// Check if user is authenticated
  Future<bool> isAuthenticated();

  /// Get current access token
  Future<String?> getAccessToken();

  /// Get current user profile
  Future<UserModel> getCurrentUser();

  /// Update user profile
  Future<UserModel> updateUser({
    required int userId,
    String? email,
    String? username,
    String? fullName,
    String? password,
    String? profilePicture,
    bool? isActive,
  });
}
