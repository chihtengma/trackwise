import 'package:dio/dio.dart';

/// Interceptor to add authentication token to requests
class AuthInterceptor extends Interceptor {
  final String? Function() getToken;

  AuthInterceptor({required this.getToken});

  @override
  void onRequest(RequestOptions options, RequestInterceptorHandler handler) {
    final token = getToken();
    
    if (token != null) {
      options.headers['Authorization'] = 'Bearer $token';
    }
    
    handler.next(options);
  }
}

/// Interceptor for logging requests/responses (for development)
class LoggingInterceptor extends Interceptor {
  final bool enabled;

  LoggingInterceptor({this.enabled = true});

  @override
  void onRequest(RequestOptions options, RequestInterceptorHandler handler) {
    if (enabled) {
      print('🌐 REQUEST[${options.method}] => PATH: ${options.path}');
      if (options.data != null) {
        print('📤 DATA: ${options.data}');
      }
      if (options.queryParameters.isNotEmpty) {
        print('🔍 QUERY: ${options.queryParameters}');
      }
    }
    handler.next(options);
  }

  @override
  void onResponse(Response response, ResponseInterceptorHandler handler) {
    if (enabled) {
      print(
        '✅ RESPONSE[${response.statusCode}] => PATH: ${response.requestOptions.path}',
      );
      if (response.data != null) {
        print('📥 DATA: ${response.data}');
      }
    }
    handler.next(response);
  }

  @override
  void onError(DioException err, ErrorInterceptorHandler handler) {
    if (enabled) {
      print('❌ ERROR[${err.response?.statusCode}] => PATH: ${err.requestOptions.path}');
      print('💥 MESSAGE: ${err.message}');
      if (err.response?.data != null) {
        print('📥 ERROR DATA: ${err.response?.data}');
      }
    }
    handler.next(err);
  }
}
