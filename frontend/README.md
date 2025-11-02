# 🚇 TrackWise Flutter Frontend

> Flutter mobile application for TrackWise - NYC Transit AI Assistant

[![Flutter](https://img.shields.io/badge/Flutter-3.24+-blue.svg)](https://flutter.dev)
[![Dart](https://img.shields.io/badge/Dart-3.5+-blue.svg)](https://dart.dev)

---

## 📋 Overview

TrackWise Flutter frontend provides a comprehensive API client architecture for interacting with the TrackWise FastAPI backend. The app offers real-time transit data, weather information, and AI-powered route recommendations for NYC commuters.

### ✨ Features

- 🔐 **Secure Authentication** - JWT-based auth with secure token storage
- 🚇 **Real-time Transit Data** - Live MTA subway and bus information
- 🌤️ **Weather Integration** - Current weather conditions for commute planning
- 💾 **Saved Routes** - Save and manage favorite transit routes
- 📱 **Modern UI** - Clean Material Design 3 interface
- 🏗️ **Clean Architecture** - Separation of concerns with repositories, data sources, and domain models

---

## 🏗️ Architecture

The app follows **Clean Architecture** principles with clear separation of concerns:

```
lib/
├── core/                    # Core utilities and configuration
│   ├── config/             # App configuration (API endpoints, etc.)
│   ├── di/                 # Dependency injection (GetIt)
│   ├── exceptions/         # Custom exception types
│   └── interceptors/       # Dio interceptors (auth, logging)
├── data/                   # Data layer
│   ├── datasources/        # Remote & local data sources
│   ├── models/             # Data models (JSON serializable)
│   └── repositories/       # Repository implementations
├── domain/                 # Domain layer
│   └── repositories/       # Repository interfaces
└── presentation/           # UI layer (to be implemented)
    ├── screens/           # App screens
    ├── widgets/           # Reusable widgets
    └── providers/         # State management (future)
```

---

## 🚀 Getting Started

### Prerequisites

- **Flutter SDK**: 3.24+ with Dart 3.5+
- **Backend**: TrackWise FastAPI backend running
- **IDE**: VS Code or Android Studio with Flutter extensions

### Installation

1. **Clone the repository** (if not already cloned)

   ```bash
   git clone <your-repo-url>
   cd TrackWise/frontend
   ```

2. **Install dependencies**

   ```bash
   flutter pub get
   ```

3. **Configure environment variables**

   ```bash
   cp .env.example .env
   ```

   Edit `.env` with your backend configuration:

   ```bash
   # Backend API Configuration
   API_BASE_URL=http://localhost:8000  # Change to your backend URL
   
   # Environment
   ENVIRONMENT=development
   ```

4. **Generate code** (if needed)

   ```bash
   flutter pub run build_runner build --delete-conflicting-outputs
   ```

5. **Run the app**

   ```bash
   # iOS
   flutter run -d ios

   # Android
   flutter run -d android

   # Web (for testing)
   flutter run -d chrome

   # Desktop
   flutter run -d macos
   flutter run -d windows
   flutter run -d linux
   ```

---

## 📦 Dependencies

### Core Dependencies

| Package | Purpose |
|---------|---------|
| `dio` | HTTP client for API calls |
| `get_it` | Dependency injection |
| `json_serializable` | JSON serialization |
| `flutter_dotenv` | Environment configuration |
| `flutter_secure_storage` | Secure token storage |
| `shared_preferences` | Local preferences |

### Development Dependencies

| Package | Purpose |
|---------|---------|
| `build_runner` | Code generation |
| `json_serializable` | JSON model generation |
| `flutter_lints` | Linting rules |

---

## 🔌 API Integration

### Authentication

```dart
import 'package:trackwise_app/core/di/service_locator.dart';
import 'package:trackwise_app/domain/repositories/auth_repository.dart';

final authRepo = getIt<AuthRepository>();

// Register
await authRepo.register(
  email: 'user@example.com',
  username: 'johndoe',
  password: 'SecurePass123!',
  fullName: 'John Doe',
);

// Login
await authRepo.login(
  email: 'user@example.com',
  password: 'SecurePass123!',
);

// Logout
await authRepo.logout();

// Check auth status
final isAuth = await authRepo.isAuthenticated();
```

### Saved Routes

```dart
import 'package:trackwise_app/core/di/service_locator.dart';
import 'package:trackwise_app/data/datasources/api_service.dart';
import 'package:trackwise_app/data/models/saved_route_model.dart';

final apiService = getIt<ApiService>();

// Get all saved routes
final routesResponse = await apiService.getSavedRoutes();

// Create a route
final newRoute = await apiService.createSavedRoute(
  SavedRouteCreate(
    name: 'Home to Work',
    origin: 'Times Sq-42 St',
    destination: 'Grand Central-42 St',
    isFavorite: true,
  ),
);

// Update route
await apiService.updateSavedRoute(
  1,
  SavedRouteUpdate(name: 'Updated Name'),
);

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
// Get current weather
final weather = await apiService.getCurrentWeather(
  location: 'New York',
  units: 'metric',
);

print('Temperature: ${weather.tempCelsius}°C');
print('Condition: ${weather.condition}');
```

---

## 🧪 Testing

```bash
# Run all tests
flutter test

# Run with coverage
flutter test --coverage

# Generate coverage report (requires lcov)
genhtml coverage/lcov.info -o coverage/html
open coverage/html/index.html
```

---

## 🛠️ Development

### Code Generation

After modifying models with `@JsonSerializable`:

```bash
flutter pub run build_runner build --delete-conflicting-outputs
```

### Watch Mode

For automatic generation during development:

```bash
flutter pub run build_runner watch --delete-conflicting-outputs
```

### Linting

```bash
flutter analyze
```

### Formatting

```bash
flutter format .
```

---

## 📱 Platform Support

| Platform | Status |
|----------|--------|
| iOS | ✅ Supported |
| Android | ✅ Supported |
| Web | ✅ Supported (testing) |
| macOS | ✅ Supported |
| Windows | ✅ Supported |
| Linux | ✅ Supported |

---

## 🔐 Security

- **Token Storage**: JWT tokens stored securely using `flutter_secure_storage`
- **HTTPS**: All API calls use HTTPS in production
- **Token Interception**: Automatic token injection via Dio interceptor
- **Error Handling**: Comprehensive error handling with custom exceptions

---

## 🐛 Troubleshooting

### Build Issues

```bash
# Clean build
flutter clean
flutter pub get
flutter pub run build_runner build --delete-conflicting-outputs
```

### Connection Issues

- Ensure backend is running on configured URL
- Check `.env` file has correct `API_BASE_URL`
- Verify backend CORS settings allow your origin

### JSON Generation Issues

```bash
# Delete generated files
find . -name "*.g.dart" -delete

# Regenerate
flutter pub run build_runner build --delete-conflicting-outputs
```

---

## 📚 Additional Resources

- [TrackWise Backend README](../backend/README.md)
- [Flutter Documentation](https://docs.flutter.dev/)
- [Dio HTTP Client](https://pub.dev/packages/dio)
- [GetIt Dependency Injection](https://pub.dev/packages/get_it)

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License.

---

**Made with ❤️ for NYC commuters**
