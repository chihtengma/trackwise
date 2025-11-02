import 'package:flutter_secure_storage/flutter_secure_storage.dart';

/// Local data source for authentication tokens
class AuthLocalDataSource {
  static const _storage = FlutterSecureStorage();
  
  // Storage keys
  static const String _accessTokenKey = 'access_token';
  static const String _userEmailKey = 'user_email';
  
  // In-memory cache for token (updated on login/logout)
  String? _cachedToken;

  /// Save access token
  Future<void> saveAccessToken(String token) async {
    _cachedToken = token; // Update cache
    await _storage.write(key: _accessTokenKey, value: token);
  }

  /// Get access token
  Future<String?> getAccessToken() async {
    return await _storage.read(key: _accessTokenKey);
  }

  /// Get access token synchronously (for interceptors)
  String? getAccessTokenSync() {
    return _cachedToken;
  }

  /// Save user email
  Future<void> saveUserEmail(String email) async {
    await _storage.write(key: _userEmailKey, value: email);
  }

  /// Get user email
  Future<String?> getUserEmail() async {
    return await _storage.read(key: _userEmailKey);
  }

  /// Clear all auth data
  Future<void> clearAuthData() async {
    _cachedToken = null;
    await _storage.deleteAll();
  }

  /// Check if user is authenticated
  Future<bool> isAuthenticated() async {
    final token = await getAccessToken();
    return token != null && token.isNotEmpty;
  }
}
