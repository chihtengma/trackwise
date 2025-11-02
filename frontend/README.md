# TrackWise Frontend

Flutter mobile application for TrackWise - NYC Transit AI Assistant.

## 🚀 Quick Start

```bash
# Install dependencies
flutter pub get

# Run the app
flutter run

# Build for production
flutter build ios
flutter build apk
```

## 📋 Prerequisites

- Flutter 3.5+
- Dart 3.5+
- iOS: Xcode 14+, iOS 12.0+
- Android: Android Studio, minSdkVersion 21

## 🛠️ Setup

### 1. Environment Configuration

Update `.env` file with your backend URL:

```bash
# For iOS Simulator/Android Emulator
API_BASE_URL=http://localhost:8000

# For physical device (use your computer's IP)
API_BASE_URL=http://YOUR_IP:8000
```

### 2. Platform Setup

#### iOS
```bash
cd ios
pod install
```

#### Android
Ensure Android Studio and emulator are configured.

### 3. Run the App

```bash
# Debug mode
flutter run

# Release mode
flutter run --release

# Specific device
flutter run -d iPhone_15_Pro
flutter run -d emulator-5554
```

## 📱 Features

- **Onboarding Flow** - Beautiful introduction screens
- **User Authentication** - Login/Signup with JWT
- **Real-time Transit Data** - Live MTA updates
- **Weather Integration** - Current conditions
- **Saved Routes** - Favorite route management
- **Offline Support** - Cached data access

## 🏗️ Project Structure

```
lib/
├── core/               # Core utilities
│   ├── config/        # App configuration
│   ├── di/            # Dependency injection
│   └── exceptions/    # Error handling
├── data/              # Data layer
│   ├── datasources/   # API & local sources
│   ├── models/        # Data models
│   └── repositories/  # Repository implementations
├── domain/            # Business logic
│   └── repositories/  # Repository interfaces
└── presentation/      # UI layer
    ├── auth/          # Login/Signup screens
    ├── onboarding/    # Onboarding screens
    ├── screens/       # App screens
    └── widgets/       # Reusable components
```

## 🎨 UI Screens

| Screen | Description | Status |
|--------|-------------|--------|
| Onboarding | App introduction | ✅ Complete |
| Login | User authentication | ✅ Complete |
| Signup | User registration | ✅ Complete |
| Home | Main dashboard | 🚧 In Progress |
| Routes | Saved routes list | 📋 Planned |
| Settings | User preferences | 📋 Planned |

## 🔧 Development

### Code Generation

Generate JSON serialization code:
```bash
flutter pub run build_runner build --delete-conflicting-outputs
```

### Testing

```bash
# Run all tests
flutter test

# Run with coverage
flutter test --coverage

# Run specific test
flutter test test/auth_test.dart
```

### Building

```bash
# iOS
flutter build ios --release

# Android APK
flutter build apk --release

# Android App Bundle
flutter build appbundle --release
```

## 📦 Key Dependencies

| Package | Purpose |
|---------|---------|
| `dio` | HTTP client |
| `get_it` | Dependency injection |
| `google_fonts` | Typography |
| `shared_preferences` | Local storage |
| `flutter_secure_storage` | Secure token storage |
| `json_annotation` | JSON serialization |

## 🎨 Design System

### Colors
- Primary: `#6366F1` (Indigo)
- Secondary: `#8B5CF6` (Purple)
- Background: `#F5F7FA`
- Text Dark: `#2D3748`
- Text Light: `#718096`
- Success: `#10B981`
- Error: `#E53935`

### Typography
- Headers: Poppins
- Body: Inter

## 🔐 Authentication Flow

1. User enters credentials
2. App sends login request to backend
3. Backend returns JWT token
4. Token stored in secure storage
5. Token added to all API requests
6. Auto-refresh on 401 responses

## 🚨 Troubleshooting

### Build Issues

```bash
# Clean and rebuild
flutter clean
flutter pub get
flutter run
```

### iOS Pod Issues

```bash
cd ios
rm -rf Pods Podfile.lock
pod install
```

### Android Gradle Issues

```bash
cd android
./gradlew clean
cd ..
flutter run
```

### API Connection Failed

1. Check backend is running: `http://localhost:8000/docs`
2. Update `.env` with correct API_BASE_URL
3. For physical devices, use computer's IP address

## 📝 Environment Variables

Create `.env` file in project root:

```bash
# API Configuration
API_BASE_URL=http://localhost:8000

# Environment
ENVIRONMENT=development
```

## 🧪 Testing Credentials

For development testing:
```
Email: test@trackwise.com
Password: Test123!
```

## 📚 Additional Resources

- [Flutter Documentation](https://docs.flutter.dev)
- [Dart Documentation](https://dart.dev/guides)
- [Material Design 3](https://m3.material.io)

---

For backend setup, see [backend/README.md](../backend/README.md)

For project overview, see [root README.md](../README.md)