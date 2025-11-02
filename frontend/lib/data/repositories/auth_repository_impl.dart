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
}
