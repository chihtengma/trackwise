# 🚇 TrackWise - NYC Transit AI Assistant

An intelligent transit application that combines real-time MTA data with AI-powered recommendations to optimize NYC commutes. Features live subway updates, weather-aware route planning, and personalized transit insights.

## ✨ Key Features

- 🚊 **Real-time MTA Updates** - Live subway and bus tracking
- 🌤️ **Weather-Aware Planning** - Commute suggestions based on weather
- 🤖 **AI Recommendations** - Smart route optimization
- 📍 **Saved Routes** - Quick access to frequent destinations
- 🔔 **Smart Notifications** - Alerts for delays and disruptions
- 🔐 **Secure Authentication** - JWT-based user accounts

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Backend** | FastAPI (Python 3.12+) |
| **Frontend** | Flutter (Dart) |
| **Database** | PostgreSQL 16+ with SQLAlchemy |
| **Cache** | Redis |
| **Authentication** | JWT with Argon2 hashing |
| **APIs** | MTA GTFS-RT, OpenWeatherMap |
| **Container** | Docker & Docker Compose |

## 📁 Project Structure

```
TrackWise/
├── backend/                 # FastAPI backend server
│   ├── app/                # Core application code
│   ├── alembic/            # Database migrations
│   ├── docker-compose.yml  # Docker services setup
│   └── Makefile            # Automation commands
│
├── frontend/               # Flutter mobile app
│   ├── lib/               # Dart source code
│   ├── assets/            # Images and resources
│   └── pubspec.yaml       # Flutter dependencies
│
└── README.md              # This file
```

## 🚀 Quick Start

### Prerequisites

- **Backend**: Python 3.12+, Docker & Docker Compose
- **Frontend**: Flutter 3.5+, Dart 3.5+
- **Mobile**: iOS Simulator/Device or Android Emulator/Device

### One-Command Setup

```bash
# Clone the repository
git clone https://github.com/chihtengma/trackwise.git
cd TrackWise

# Start backend (Docker)
cd backend
make docker-up    # Start PostgreSQL & Redis
make install      # Install Python dependencies
make db-upgrade   # Run database migrations
make run          # Start server on http://localhost:8000

# Start frontend (new terminal)
cd frontend
flutter pub get   # Install dependencies
flutter run       # Launch app
```

## 📱 Mobile App Screens

| Screen | Description | Status |
|--------|-------------|--------|
| Onboarding | Welcome flow with app introduction | ✅ Complete |
| Authentication | Login & Signup with validation | ✅ Complete |
| Home Dashboard | Real-time transit overview | 🚧 In Progress |
| Route Planning | AI-powered trip suggestions | 📋 Planned |
| Saved Routes | Favorite destinations | 📋 Planned |

## 🔧 Development

### Backend Commands

```bash
cd backend
make docker-up      # Start Docker containers
make run            # Run server (Docker DB)
make test           # Run test suite
make docker-status  # Check container status
```

### Frontend Commands

```bash
cd frontend
flutter run         # Run in debug mode
flutter build ios   # Build for iOS
flutter build apk   # Build for Android
flutter test        # Run tests
```

## 📚 Documentation

- **Backend Details**: See [backend/README.md](backend/README.md)
- **Frontend Details**: See [frontend/README.md](frontend/README.md)
- **API Docs**: `http://localhost:8000/docs` (when server is running)

## 🧪 Testing

The project includes comprehensive test coverage:

```bash
# Backend tests
cd backend && make test

# Frontend tests
cd frontend && flutter test

# API integration tests
cd backend && make test-api
```

## 🔐 Security

- Password hashing with Argon2
- JWT token authentication
- Environment-based configuration
- Secure storage for mobile tokens
- CORS protection

## 🌐 External Services

| Service | Purpose | Required |
|---------|---------|----------|
| MTA GTFS-RT | Real-time transit data | ✅ No API key |
| OpenWeatherMap | Weather conditions | ✅ API key required |
| MTA Bus Time | Bus tracking | ⚪ Optional |

## 🤝 Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch
3. Write tests for new features
4. Ensure all tests pass
5. Submit a pull request

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/chihtengma/trackwise/issues)
- **Email**: chihtengma416@gmail.com

## 🎯 Roadmap

- [x] User authentication system
- [x] Onboarding flow
- [ ] Real-time subway tracking
- [ ] AI route recommendations
- [ ] Push notifications
- [ ] Offline mode
- [ ] Apple Watch app
- [ ] Transit history analytics

---

**Built with ❤️ for NYC commuters**