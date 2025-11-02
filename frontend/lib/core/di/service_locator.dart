import 'package:dio/dio.dart';
import 'package:get_it/get_it.dart';

import '../config/app_config.dart';
import '../interceptors/auth_interceptor.dart';
import '../../data/datasources/api_service.dart';
import '../../data/datasources/auth_local_datasource.dart';
import '../../data/datasources/auth_remote_datasource.dart';
import '../../data/repositories/auth_repository_impl.dart';
import '../../domain/repositories/auth_repository.dart';

/// Service locator for dependency injection
final getIt = GetIt.instance;

/// Initialize all dependencies
Future<void> setupServiceLocator() async {
  // Register configuration
  final appConfig = AppConfig();
  await appConfig.initialize();
  getIt.registerLazySingleton<AppConfig>(() => appConfig);

  // Register local storage
  final authLocalDataSource = AuthLocalDataSource();
  getIt.registerLazySingleton<AuthLocalDataSource>(() => authLocalDataSource);

  // Register Dio client with interceptors
  final dio = _createDioClient(appConfig, authLocalDataSource);
  getIt.registerLazySingleton<Dio>(() => dio);

  // Register remote data sources
  getIt.registerLazySingleton<AuthRemoteDataSource>(
    () => AuthRemoteDataSource(dio: dio, config: appConfig),
  );

  // Register API service
  getIt.registerLazySingleton<ApiService>(
    () => ApiService(dio: dio, config: appConfig),
  );

  // Register repositories
  getIt.registerLazySingleton<AuthRepository>(
    () => AuthRepositoryImpl(
      remoteDataSource: getIt(),
      localDataSource: getIt(),
      config: appConfig,
    ),
  );
}

/// Create configured Dio client
Dio _createDioClient(AppConfig config, AuthLocalDataSource authLocalDataSource) {
  final dio = Dio(
    BaseOptions(
      baseUrl: config.apiBaseUrl,
      connectTimeout: const Duration(seconds: 30),
      receiveTimeout: const Duration(seconds: 30),
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
    ),
  );

  // Add interceptors
  dio.interceptors.addAll([
    AuthInterceptor(
      getToken: () => authLocalDataSource.getAccessTokenSync(),
    ),
  ]);

  return dio;
}
