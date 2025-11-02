# TrackWise

A real-time transit tracking application for NYC commuters, providing live subway updates, weather information, and route management.

## Project Structure

```
TrackWise/
├── backend/          # FastAPI backend application
│   ├── app/         # Application code
│   ├── alembic/     # Database migrations
│   └── tests/       # Backend tests
└── frontend/        # Flutter mobile application
    ├── lib/         # Flutter application code
    ├── android/     # Android-specific files
    └── ios/         # iOS-specific files
```

## Features

- **Real-time Transit Updates**: Live NYC subway status and arrival times
- **Weather Integration**: Current weather conditions affecting your commute
- **Route Management**: Save and manage frequently used routes
- **User Authentication**: Secure user accounts with JWT authentication
- **Background Updates**: Scheduled notifications for route disruptions

## Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Cache**: Redis for performance optimization
- **Authentication**: JWT tokens
- **Task Scheduling**: APScheduler for background tasks

### Frontend
- **Framework**: Flutter
- **State Management**: Provider/Riverpod
- **HTTP Client**: Dio
- **Local Storage**: Shared Preferences

## Getting Started

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run database migrations:
```bash
alembic upgrade head
```

6. Start the server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install Flutter dependencies:
```bash
flutter pub get
```

3. Set up environment configuration:
```bash
cp .env.example .env
# Edit .env with your API URL
```

4. Run the application:
```bash
flutter run
```

## API Documentation

When the backend is running, you can access:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
flutter test
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Contact

Project Link: [https://github.com/chihtengma/trackwise](https://github.com/chihtengma/trackwise)