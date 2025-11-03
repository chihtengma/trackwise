import '../../core/config/app_config.dart';
import '../../core/exceptions/api_exception.dart';
import '../../domain/repositories/auth_repository.dart';
import '../datasources/auth_local_datasource.dart';
import '../datasources/auth_remote_datasource.dart';
import '../models/user_model.dart';

/// Implementation of authentication repository
class AuthRepositoryImpl implements AuthRepository {
  final AuthRemoteDataSource remoteDataSource;
  final AuthLocalDataSource localDataSource;
  final AppConfig config;

  AuthRepositoryImpl({
    required this.remoteDataSource,
    required this.localDataSource,
    required this.config,
  });

  @override
  Future<UserModel> register({
    required String email,
    required String username,
    required String password,
    String? fullName,
  }) async {
    try {
      final user = await remoteDataSource.register(
        email: email,
        username: username,
        password: password,
        fullName: fullName,
      );
      return user;
    } catch (e) {
      if (e is ApiException) {
        rethrow;
      }
      throw UnknownException(message: 'Registration failed: ${e.toString()}');
    }
  }

  @override
  Future<bool> login({
    required String email,
    required String password,
  }) async {
    try {
      final tokenResponse = await remoteDataSource.login(
        email: email,
        password: password,
      );

      // Save token and email to local storage
      await localDataSource.saveAccessToken(tokenResponse.accessToken);
      await localDataSource.saveUserEmail(email);

      return true;
    } catch (e) {
      if (e is ApiException) {
        rethrow;
      }
      throw UnknownException(message: 'Login failed: ${e.toString()}');
    }
  }

  @override
  Future<bool> socialLogin({
    required String provider,
    required String idToken,
    String? accessToken,
    String? authorizationCode,
    String? nonce,
  }) async {
    try {
      final tokenResponse = await remoteDataSource.socialLogin(
        provider: provider,
        idToken: idToken,
        accessToken: accessToken,
        authorizationCode: authorizationCode,
        nonce: nonce,
      );

      // Save token and email to local storage
      await localDataSource.saveAccessToken(tokenResponse.accessToken);
      // Extract email from token response if available, or from user data
      final email = tokenResponse.user?.email ?? '';
      if (email.isNotEmpty) {
        await localDataSource.saveUserEmail(email);
      }

      return true;
    } catch (e) {
      if (e is ApiException) {
        rethrow;
      }
      throw UnknownException(message: 'Social login failed: ${e.toString()}');
    }
  }

  @override
  Future<void> logout() async {
    await localDataSource.clearAuthData();
  }

  @override
  Future<bool> isAuthenticated() async {
    return await localDataSource.isAuthenticated();
  }

  @override
  Future<String?> getAccessToken() async {
    return await localDataSource.getAccessToken();
  }

  @override
  Future<UserModel> getCurrentUser() async {
    try {
      return await remoteDataSource.getCurrentUser();
    } catch (e) {
      if (e is ApiException) {
        rethrow;
      }
      throw UnknownException(message: 'Failed to get user profile: ${e.toString()}');
    }
  }

  @override
  Future<UserModel> updateUser({
    required int userId,
    String? email,
    String? username,
    String? fullName,
    String? password,
    String? profilePicture,
    bool? isActive,
  }) async {
    try {
      return await remoteDataSource.updateUser(
        userId: userId,
        email: email,
        username: username,
        fullName: fullName,
        password: password,
        profilePicture: profilePicture,
        isActive: isActive,
      );
    } catch (e) {
      if (e is ApiException) {
        rethrow;
      }
      throw UnknownException(message: 'Failed to update user profile: ${e.toString()}');
    }
  }
}
