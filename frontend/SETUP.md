# TrackWise Flutter API Client Setup

This document provides a comprehensive guide to the Flutter API client architecture that has been integrated with the TrackWise backend.

## 🎯 Architecture Overview

The Flutter frontend follows **Clean Architecture** principles with clear separation of concerns:

```
lib/
├── core/                    # Core utilities and configuration
│   ├── config/             
│   │   └── app_config.dart         # API endpoints, app configuration
│   ├── di/                 
│   │   └── service_locator.dart    # Dependency injection setup
│   ├── exceptions/         
│   │   └── api_exception.dart      # Custom exception types
│   └── interceptors/       
│       └── auth_interceptor.dart   # JWT token injection
├── data/                   # Data layer
│   ├── datasources/        
│   │   ├── api_service.dart                # Main API service
│   │   ├── auth_local_datasource.dart      # Secure token storage
│   │   └── auth_remote_datasource.dart     # Auth API calls
│   ├── models/             
│   │   ├── user_model.dart                 # User models
│   │   ├── saved_route_model.dart          # Saved routes models
│   │   ├── transit_model.dart              # Transit data models
│   │   └── weather_model.dart              # Weather models
│   └── repositories/       
│       └── auth_repository_impl.dart       # Auth repository
├── domain/                 # Domain layer
│   └── repositories/       
│       └── auth_repository.dart            # Auth interface
└── presentation/           # UI layer (ready for implementation)
```

## ✅ What's Implemented

### 1. API Client Infrastructure ✅

- ✅ Dio HTTP client with interceptors
- ✅ Authentication token management
- ✅ Custom exception handling
- ✅ Request/response logging
- ✅ Environment configuration

### 2. Models & Serialization ✅

- ✅ User models (User, UserCreate, UserUpdate, Token)
- ✅ Saved route models (SavedRoute, SavedRouteCreate, SavedRouteUpdate)
- ✅ Transit models (TripUpdate, RouteQuery, RouteResponse)
- ✅ Weather models (WeatherCurrentResponse, WeatherQuery)
- ✅ JSON serialization with code generation

### 3. Authentication ✅

- ✅ Registration endpoint
- ✅ Login endpoint (OAuth2 form-data)
- ✅ JWT token storage (secure storage + in-memory cache)
- ✅ Logout functionality
- ✅ Authentication state checking

### 4. API Services ✅

- ✅ User profile management
- ✅ Saved routes CRUD operations
- ✅ Transit data fetching
- ✅ Weather data fetching
- ✅ Query route planning

### 5. Dependency Injection ✅

- ✅ GetIt service locator setup
- ✅ Lazy singleton registration
- ✅ Automatic token injection

## 🚀 Quick Start

1. **Ensure backend is running**:

   ```bash
   cd ../backend
   make run
   ```

2. **Configure frontend**:

   ```bash
   cp .env.example .env
   # Edit .env to match your backend URL
   ```

3. **Install dependencies**:

   ```bash
   flutter pub get
   ```

4. **Generate code** (if models changed):

   ```bash
   flutter pub run build_runner build --delete-conflicting-outputs
   ```

5. **Run the app**:

   ```bash
   flutter run
   ```

## 📝 Usage Examples

### Authentication

```dart
import 'package:trackwise_app/core/di/service_locator.dart';
import 'package:trackwise_app/domain/repositories/auth_repository.dart';

final authRepo = getIt<AuthRepository>();

// Register new user
await authRepo.register(
  email: 'john@example.com',
  username: 'johndoe',
  password: 'SecurePass123!',
  fullName: 'John Doe',
);

// Login
await authRepo.login(
  email: 'john@example.com',
  password: 'SecurePass123!',
);

// Check auth status
final isAuth = await authRepo.isAuthenticated();

// Logout
await authRepo.logout();
```

### Saved Routes

```dart
import 'package:trackwise_app/data/datasources/api_service.dart';
import 'package:trackwise_app/data/models/saved_route_model.dart';

final apiService = getIt<ApiService>();

// Get all saved routes
final routes = await apiService.getSavedRoutes();

// Create route
final newRoute = await apiService.createSavedRoute(
  SavedRouteCreate(
    name: 'Home to Work',
    origin: 'Times Sq-42 St',
    destination: 'Grand Central-42 St',
    isFavorite: true,
  ),
);

// Update route
await apiService.updateSavedRoute(1, SavedRouteUpdate(name: 'Updated'));

// Delete route
await apiService.deleteSavedRoute(1);
```

### Transit Data

```dart
// Get route updates
final updates = await apiService.getRouteUpdates('A');

// Query routes
final response = await apiService.queryRoutes(
  RouteQuery(
    origin: 'Times Sq-42 St',
    destination: 'Grand Central-42 St',
    maxRoutes: 3,
  ),
);
```

### Weather

```dart
final weather = await apiService.getCurrentWeather(
  location: 'New York',
  units: 'metric',
);
```

## 🔐 Security Features

- **Secure Token Storage**: JWT tokens stored using `flutter_secure_storage`
- **In-Memory Cache**: Fast token access for interceptors
- **Automatic Injection**: Tokens automatically added to requests
- **HTTPS Support**: All API calls use secure connections
- **Error Handling**: Comprehensive exception handling

## 🧪 Testing

```bash
# Run all tests
flutter test

# Run with coverage
flutter test --coverage
```

## 📦 Dependencies

### Core

- `dio`: HTTP client
- `get_it`: Dependency injection
- `json_annotation/serializable`: JSON handling
- `flutter_dotenv`: Environment config
- `flutter_secure_storage`: Secure storage

### Dev

- `build_runner`: Code generation
- `flutter_lints`: Linting

## 🎨 Next Steps

### UI Implementation

- [ ] Create auth screens (login/register)
- [ ] Design saved routes UI
- [ ] Build transit map interface
- [ ] Add weather display widgets
- [ ] Implement navigation flow

### State Management

- [ ] Add Riverpod or Bloc
- [ ] Create auth provider/state
- [ ] Add routes state management
- [ ] Implement caching layer

### Features

- [ ] Route favorites UI
- [ ] Real-time updates polling
- [ ] Push notifications
- [ ] Offline mode
- [ ] Widget-based route cards

## 📚 API Endpoints Reference

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/auth/register` | POST | User registration |
| `/api/v1/auth/login` | POST | User login |
| `/api/v1/users/me` | GET | Get current user |
| `/api/v1/users/{id}` | GET/PATCH | User operations |
| `/api/v1/saved-routes` | GET/POST | Saved routes list |
| `/api/v1/saved-routes/{id}` | GET/PUT/DELETE | Route operations |
| `/api/v1/transit/routes/{id}/updates` | GET | Route updates |
| `/api/v1/transit/routes/query` | POST | Route planning |
| `/api/v1/weather/current` | GET | Current weather |
| `/api/v1/weather/query` | POST | Weather query |

## 🐛 Common Issues

### Token Not Being Sent

**Solution**: Check that `saveAccessToken` is called after login and cache is initialized.

### Connection Errors

**Solution**: Verify backend is running and `.env` has correct `API_BASE_URL`.

### JSON Serialization Errors

**Solution**: Run `flutter pub run build_runner build --delete-conflicting-outputs`.

### Build Errors

**Solution**: Clean and rebuild:

```bash
flutter clean
flutter pub get
flutter pub run build_runner build --delete-conflicting-outputs
```

## 📖 Additional Resources

- [Backend API Docs](http://localhost:8000/docs)
- [Flutter Documentation](https://docs.flutter.dev/)
- [Dio Package](https://pub.dev/packages/dio)
- [GetIt Package](https://pub.dev/packages/get_it)

---

**Status**: ✅ API Client Architecture Complete - Ready for UI Development
