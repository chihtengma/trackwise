# TrackWise Backend

FastAPI backend service for TrackWise - NYC Transit AI Assistant.

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.120-green.svg)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16+-blue.svg)](https://postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://docker.com)
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
- **Docker & Docker Compose** (recommended) OR **PostgreSQL 16+** (local)
- **Redis** (optional, included in Docker setup)

### Database Options

TrackWise backend supports two database configurations:

#### Option 1: Docker PostgreSQL (Recommended)
- Isolated development environment
- No local PostgreSQL installation needed
- Includes Redis for caching
- Easy cleanup and reset

#### Option 2: Local PostgreSQL (Homebrew/Native)
- Uses your system's PostgreSQL installation
- Good for existing PostgreSQL users
- Requires manual PostgreSQL setup

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/chihtengma/trackwise.git
   cd TrackWise/backend
   ```

2. **Install Python dependencies**

   ```bash
   make install
   ```

   This will:
   - Create a virtual environment (`.venv`)
   - Install all required packages from `requirements.txt`
   - Set up the development environment

3. **Choose your database setup**

   #### For Docker Database (Recommended):
   ```bash
   # Start Docker containers
   make docker-up

   # Run database migrations
   make db-upgrade

   # Start server (uses Docker DB by default)
   make run
   ```

   #### For Local Database:
   ```bash
   # Ensure PostgreSQL is running
   brew services start postgresql@16  # macOS with Homebrew

   # Create database
   createdb trackwise

   # Run migrations
   make db-upgrade

   # Start server with local DB
   make run-local
   ```

4. **Configure API keys** (Optional)

   ```bash
   # Copy environment template
   cp .env.example .env

   # Edit .env to add your API keys:
   OPENWEATHER_API_KEY=your_openweather_api_key
   MTA_BUS_API_KEY=your_mta_bus_api_key_if_needed
   ```

The API will be available at:
- **Main API**: <http://localhost:8000>
- **Interactive Docs**: <http://localhost:8000/docs>
- **Alternative Docs**: <http://localhost:8000/redoc>

---

## 📋 Available Commands

### Makefile Commands

| Command | Description | Database |
|---------|-------------|----------|
| `make install` | Set up virtual environment and install dependencies | - |
| `make run` | Start server with **Docker** database (default) | Docker |
| `make run-local` | Start server with **local** database | Local |
| `make test` | Run the full test suite with coverage | Current |
| `make test-api` | Run API integration tests | Current |
| `make docker-up` | Start Docker PostgreSQL & Redis containers | Docker |
| `make docker-down` | Stop all Docker containers | Docker |
| `make docker-status` | Check Docker containers status | Docker |
| `make docker-db` | Connect to Docker PostgreSQL shell | Docker |
| `make db-create` | Create database if it doesn't exist | Current |
| `make migrate` | Create a new database migration | Current |
| `make db-upgrade` | Apply all pending migrations | Current |
| `make db-downgrade` | Rollback the last migration | Current |
| `make format` | Format code with Black | - |
| `make lint` | Run Flake8 and MyPy linting | - |
| `make clean` | Remove generated files and caches | - |

### Interactive Scripts

Located in `scripts/` directory - these provide interactive menus and detailed feedback:

| Script | Purpose | Usage |
|--------|---------|-------|
| `start_server.sh` | Interactive server starter with DB selection | `./scripts/start_server.sh` |
| `setup_database.sh` | Database setup wizard (Docker or Local) | `./scripts/setup_database.sh` |
| `check_database.sh` | Check DB connection and display user stats | `./scripts/check_database.sh` |
| `test_api.sh` | Run tests with options (unit/integration/both) | `./scripts/test_api.sh` |

---

## 🏗️ Project Structure

```text
backend/
├── alembic/                # Database migration scripts
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
│   ├── start_server.sh     # Interactive server launcher
│   ├── setup_database.sh   # Database setup wizard
│   ├── check_database.sh   # Database status checker
│   ├── test_api.sh         # Test runner with options
│   ├── create_db.py        # Python DB creation utility
│   └── test_api.py         # Python API integration tests
├── .env                    # Current environment (created from .env.docker or .env.local)
├── .env.docker             # Docker database configuration
├── .env.local              # Local database configuration
├── .env.example            # Environment template with all variables
├── docker-compose.yml      # Docker services configuration
├── alembic.ini             # Alembic configuration
├── Makefile                # Development automation commands
├── pytest.ini              # Pytest configuration
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

---

## 🔧 Configuration

### Database Configuration

The backend supports dual database configurations managed through environment files:

#### Docker Database Configuration (`.env.docker`)
```bash
DATABASE_URL=postgresql://trackwise:trackwise_dev@localhost:5432/trackwise
```
- **User**: trackwise
- **Password**: trackwise_dev
- **Database**: trackwise
- **Host**: localhost (Docker container)
- **Port**: 5432

#### Local Database Configuration (`.env.local`)
```bash
DATABASE_URL=postgresql://your_username:@localhost:5432/trackwise
```
- **User**: Your system username
- **Password**: Empty (peer authentication)
- **Database**: trackwise
- **Host**: localhost
- **Port**: 5432

#### Switching Between Databases

**Method 1: Using Makefile (Simple)**
```bash
make run          # Uses Docker database
make run-local    # Uses local database
```

**Method 2: Using Interactive Script (Detailed)**
```bash
./scripts/start_server.sh  # Interactive menu to choose database
```

**Method 3: Manual Environment File**
```bash
cp .env.docker .env  # Use Docker database
# OR
cp .env.local .env   # Use local database
make run
```

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

## 💡 Common Workflows

### First Time Setup with Docker
```bash
make install          # Install Python dependencies
make docker-up        # Start Docker containers
make db-upgrade       # Run migrations
make run             # Start server (uses Docker DB)
```

### First Time Setup with Local Database
```bash
make install                      # Install Python dependencies
brew services start postgresql@16 # Start PostgreSQL
createdb trackwise                # Create database
make db-upgrade                   # Run migrations
make run-local                   # Start server (uses local DB)
```

### Daily Development
```bash
# With Docker
make docker-up       # Ensure containers are running
make run            # Start server

# With Local
brew services start postgresql@16  # Ensure PostgreSQL is running
make run-local                     # Start server
```

### Check Database Status
```bash
# Quick check
make docker-status   # For Docker
# OR
./scripts/check_database.sh  # Detailed status for any DB
```

### Switch Between Databases
```bash
# From Local to Docker
make docker-up
make run  # Now using Docker

# From Docker to Local
brew services start postgresql@16
make run-local  # Now using local
```

### Running Tests
```bash
make test        # Unit tests with pytest
make test-api    # API integration tests
# OR
./scripts/test_api.sh  # Interactive test menu
```

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

### Pre-commit Hooks (Optional)

Install pre-commit hooks to automatically check code quality before commits:

```bash
# Install pre-commit
pip install pre-commit

# Install git hooks
pre-commit install

# Run on all files
pre-commit run --all-files
```

Hooks check for:

- Secret detection (prevents committing real secrets)
- Code formatting (Black)
- Linting (Flake8)
- YAML syntax
- Large files
- Merge conflicts

---

## 🔐 Security

### Secrets Management

- Never commit `.env` files
- Use strong `SECRET_KEY` in production
- Rotate keys periodically
- Use environment-specific configs
- Pre-commit hooks detect secrets before commit
- CI workflow uses isolated test values only

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

View CI status: [![CI](https://github.com/chihtengma/TrackWise/actions/workflows/ci.yml/badge.svg)](https://github.com/chihtengma/TrackWise/actions/workflows/ci.yml)

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
