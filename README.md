# 🚇 TrackWise Transit AI Assistant

> An intelligent transit assistant backend powered by FastAPI, providing real-time transit data, weather information, and AI-powered recommendations for NYC commuters.

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.120-green.svg)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16+-blue.svg)](https://postgresql.org)
[![CI](https://github.com/YOUR_USERNAME/TrackWise/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_USERNAME/TrackWise/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## ✨ Features

- 🚇 **Real-time MTA Subway Data** - GTFS-Realtime feeds for all NYC subway lines
- 🚌 **MTA Bus Information** - Optional real-time bus data (API key required)
- 🌤️ **Weather Integration** - OpenWeatherMap integration for commute planning
- 🔐 **Secure Authentication** - JWT-based auth with Argon2 password hashing
- 📊 **Database Migrations** - Alembic-powered schema management
- 🧪 **Full Test Coverage** - Pytest with async support
- 📝 **Auto-generated Docs** - Interactive API documentation with Swagger/ReDoc
- 🎨 **Code Quality** - Black, Flake8, and MyPy for linting

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.12+**
- **PostgreSQL 16+**
- **Redis** (optional, for caching)
- **pip** and **venv**

### Installation

1. **Clone the repository**

   ```bash
   git clone <your-repo-url>
   cd TrackWise/backend
   ```

2. **Install dependencies**

   ```bash
   make install
   ```

   This will:
   - Create a virtual environment (`.venv`)
   - Install all required packages from `requirements.txt`
   - Set up the development environment

3. **Configure environment variables**

   ```bash
   cp .env.example .env
   ```

   Edit `.env` with your configuration:

   ```bash
   # Required: Database
   DATABASE_URL=postgresql://username:password@localhost:5432/trackwise

   # Required: Security
   SECRET_KEY=your-secret-key-here-change-in-production
   # Generate a secure key with: openssl rand -hex 32

   # Required: Weather API
   OPENWEATHER_API_KEY=your_openweather_api_key

   # Optional: MTA Bus Time API
   MTA_BUS_API_KEY=your_mta_bus_api_key_if_needed
   ```

4. **Create the database**

   ```bash
   make db-create
   ```

   This automatically creates the PostgreSQL database if it doesn't exist.

5. **Run migrations**

   ```bash
   make db-upgrade
   ```

   This applies all database schema migrations.

6. **Start the development server**

   ```bash
   make run
   ```

   The API will be available at:
   - **Main API**: <http://localhost:8000>
   - **Interactive Docs**: <http://localhost:8000/docs>
   - **Alternative Docs**: <http://localhost:8000/redoc>

---

## 📋 Available Commands

| Command | Description |
|---------|-------------|
| `make install` | Set up virtual environment and install dependencies |
| `make run` | Start the development server with auto-reload |
| `make test` | Run the full test suite with coverage |
| `make db-create` | Create database if it doesn't exist |
| `make migrate` | Create a new database migration |
| `make db-upgrade` | Apply all pending migrations |
| `make db-downgrade` | Rollback the last migration |
| `make format` | Format code with Black |
| `make lint` | Run Flake8 and MyPy linting |
| `make clean` | Remove generated files and caches |

---

## 🏗️ Project Structure

```text
backend/
├── alembic/                 # Database migration scripts
│   ├── versions/           # Migration history
│   └── env.py              # Alembic configuration
├── app/
│   ├── api/                # API routes
│   │   └── v1/
│   │       └── endpoints/  # Endpoint definitions
│   ├── core/               # Core configuration
│   │   ├── config.py       # App settings & env vars
│   │   ├── database.py     # DB engine & sessions
│   │   └── security.py     # Auth & password hashing
│   ├── models/             # SQLAlchemy ORM models
│   │   └── user.py         # User model
│   ├── schemas/            # Pydantic schemas
│   │   └── user.py         # Request/response schemas
│   ├── services/           # Business logic layer
│   ├── tests/              # Test suite
│   │   ├── conftest.py     # Pytest fixtures
│   │   ├── test_main.py    # Main endpoint tests
│   │   ├── test_auth.py    # Auth endpoint tests
│   │   └── test_users.py   # User endpoint tests
│   ├── utils/              # Utility functions
│   └── main.py             # FastAPI application
├── scripts/
│   ├── create_db.py        # Database creation utility
│   └── test_api.py         # API integration tests
├── .env.example            # Environment variables template
├── alembic.ini             # Alembic configuration
├── Makefile                # Development commands
├── pytest.ini              # Pytest configuration
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

---

## 🔧 Configuration

### Required Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@localhost:5432/trackwise` |
| `SECRET_KEY` | JWT signing key (32+ chars) | Generate with `openssl rand -hex 32` |
| `OPENWEATHER_API_KEY` | OpenWeatherMap API key | Get from [openweathermap.org](https://openweathermap.org/api) |

### Optional Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DEBUG` | Enable debug mode | `False` |
| `ENVIRONMENT` | Environment name | `development` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |
| `MTA_BUS_API_KEY` | MTA Bus Time API key | `None` |
| `REDIS_URL` | Redis connection URL | `redis://localhost:6379/0` |
| `DATABASE_ECHO` | Log SQL queries | `False` |
| `LOG_LEVEL` | Logging level | `INFO` |

### CORS Configuration

```bash
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

This accepts comma-separated origins. Use `settings.allowed_origins_list` in code to get a Python list.

---

## 🗄️ Database

### PostgreSQL Setup

The project uses PostgreSQL with async SQLAlchemy:

- **Sync Driver**: `psycopg2-binary` for migrations and sync operations
- **Async Driver**: `asyncpg` for async FastAPI endpoints
- **Migration Tool**: Alembic for schema versioning

### Creating Migrations

```bash
make migrate
# Enter migration message when prompted
```

### Applying Migrations

```bash
make db-upgrade
```

### Rollback

```bash
make db-downgrade
```

---

## 🧪 Testing

The project includes two types of tests:

### 1. Unit/Integration Tests (pytest)

Run the full test suite with coverage:

```bash
make test
```

Run specific test files:

```bash
.venv/bin/pytest app/tests/test_main.py -v --no-cov
.venv/bin/pytest app/tests/test_auth.py -v --no-cov
.venv/bin/pytest app/tests/test_users.py -v --no-cov
```

View coverage report:

```bash
# HTML report generated at: htmlcov/index.html
open htmlcov/index.html
```

### 2. API Integration Tests

For comprehensive API endpoint testing (requires running server):

```bash
# Start the server
make run

# In another terminal, run API tests
python scripts/test_api.py
# Or
make test-api
```

The API test script checks all endpoints including:

- Authentication (register, login)
- User management (CRUD operations)
- Authorization (token validation)
- Error handling

**Note**: Pytest integration tests are currently in development. The API test script (`scripts/test_api.py`) provides full coverage of all endpoints and is the recommended way to verify the API functionality.

---

## 📚 API Documentation

Once the server is running, visit:

- **Swagger UI**: <http://localhost:8000/docs>
- **ReDoc**: <http://localhost:8000/redoc>

### Example API Request

```bash
# Get API documentation
curl http://localhost:8000/openapi.json

# Health check (once implemented)
curl http://localhost:8000/health
```

---

## 🛠️ Development

### Code Formatting

```bash
make format  # Format with Black
```

### Linting

```bash
make lint  # Run Flake8 and MyPy
```

### Virtual Environment

The project uses Python venv. To activate manually:

```bash
source .venv/bin/activate  # On macOS/Linux
.venv\Scripts\activate     # On Windows
```

### Adding Dependencies

1. Add to `requirements.txt`
2. Run `make install`
3. Update version pins if needed

---

## 🔐 Security

### Secrets Management

- Never commit `.env` files
- Use strong `SECRET_KEY` in production
- Rotate keys periodically
- Use environment-specific configs

### Password Hashing

The app uses **Argon2** via `pwdlib[argon2]` for password hashing.

### JWT Tokens

- Algorithm: `HS256` (configurable)
- Default expiration: 30 minutes
- Token refresh: TBD

---

## 🌐 External APIs

### MTA Subway (No API Key Required)

Real-time subway data from GTFS-Realtime feeds:

```text
https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct/{feed_id}
```

Available Feeds:

- `gtfs` - All lines combined
- `gtfs-ace` - A, C, E, H, FS
- `gtfs-bdfm` - B, D, F, M
- `gtfs-g` - G
- `gtfs-jz` - J, Z
- `gtfs-nqrw` - N, Q, R, W
- `gtfs-l` - L
- Plus numbered lines (1-7, S, SIR)

### MTA Bus Time (API Key Required)

Optional bus data. Get an API key from:
<http://bustime.mta.info/>

### OpenWeatherMap (API Key Required)

Weather data for commute planning. Get an API key from:
<https://openweathermap.org/api>

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Development Guidelines

- Write tests for new features
- Follow PEP 8 style guide
- Update documentation as needed
- Run `make lint` before committing
- Keep commits atomic and well-described

### CI/CD

The project uses GitHub Actions for continuous integration:

- **Automated Testing**: Runs on every push and PR to `main` and `develop`
- **Code Quality**: Checks formatting with Black and linting with Flake8
- **Database Testing**: Spins up PostgreSQL container for integration tests
- **Multi-job Pipeline**: Separate jobs for tests and code formatting checks

View CI status: [![CI](https://github.com/chihtengma/TrackWise/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_USERNAME/TrackWise/actions/workflows/ci.yml)

---

## 📝 License

This project is licensed under the MIT License.

---

## 🐛 Troubleshooting

### Database Connection Issues

```bash
# Check if PostgreSQL is running
psql -l

# Verify database exists
make db-create

# Check connection string in .env
echo $DATABASE_URL
```

### Import Errors

```bash
# Ensure virtual environment is activated
source .venv/bin/activate

# Reinstall dependencies
make install
```

### Migration Issues

```bash
# Use make commands (they automatically use the right Python)
make db-upgrade

# Or ensure venv is activated before running alembic directly
source .venv/bin/activate
.venv/bin/alembic current  # Check migration status
.venv/bin/alembic history  # View migration history

# Rollback and retry
make db-downgrade
make db-upgrade
```

### Port Already in Use

```bash
# Change PORT in .env or kill the process
lsof -ti:8000 | xargs kill  # On macOS/Linux
```

---

## 📞 Support

For issues and questions:

- **GitHub Issues**: [Create an issue](../../issues)
- **Documentation**: Check `/docs` endpoint when server is running
- **Email**: [chihtengma416@gmail.com]

---

## 🎯 Roadmap

- [ ] Complete user authentication endpoints
- [ ] Add ride tracking functionality
- [ ] Implement AI-powered route recommendations
- [ ] Add push notifications for delays
- [ ] Create mobile app companion
- [ ] Add historical data analysis
- [ ] Implement favorite stations/routes

---

**Made with ❤️ for NYC commuters**
