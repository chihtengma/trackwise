.PHONY: help install run run-local test test-api clean migrate db-upgrade db-downgrade format lint db-create docker-up docker-down docker-status docker-db

# Default target - show help
help:
	@echo "📋 TrackWise Transit AI - Available Commands"
	@echo "========================================"
	@echo ""
	@echo "🐳 Docker Database Commands:"
	@echo "  make docker-up     - 🚀 Start Docker PostgreSQL & Redis"
	@echo "  make docker-down   - 🛑 Stop Docker containers"
	@echo "  make docker-status - 📊 Check Docker containers status"
	@echo "  make docker-db     - 🔍 Connect to Docker PostgreSQL shell"
	@echo ""
	@echo "🚀 Server Commands:"
	@echo "  make run           - 🐳 Run server with Docker database"
	@echo "  make run-local     - 💻 Run server with local database"
	@echo ""
	@echo "🔧 Setup & Database:"
	@echo "  make install       - 📦 Set up virtual environment and install dependencies"
	@echo "  make db-create     - 🗄️  Create database if it doesn't exist"
	@echo "  make migrate       - 🔄 Create a new database migration"
	@echo "  make db-upgrade    - ⬆️  Apply database migrations"
	@echo "  make db-downgrade  - ⬇️  Rollback last migration"
	@echo ""
	@echo "🧪 Testing & Quality:"
	@echo "  make test          - 🧪 Run tests with pytest"
	@echo "  make test-api      - 🧪 Test all API endpoints"
	@echo "  make format        - 🎨 Format code with black"
	@echo "  make lint          - 🔍 Run linting checks"
	@echo "  make clean         - 🧹 Remove generated files and caches"
	@echo ""
	@echo "Quick start: make docker-up && make run"
	@echo ""

# Install dependencies
install:
	@echo "📦 Setting up virtual environment..."
	python3 -m venv .venv
	@echo "⬆️  Upgrading pip..."
	.venv/bin/pip install --upgrade pip
	@echo "📥 Installing dependencies..."
	.venv/bin/pip install -r requirements.txt
	@echo ""
	@echo "✅ Installation complete!"
	@echo ""
	@echo "Next steps:"
	@echo "  1. Copy .env.example to .env and configure"
	@echo "  2. Run 'make db-upgrade' to set up database"
	@echo "  3. Run 'make run' to start the server"
	@echo ""

# Run development server with Docker database
run:
	@echo "🐳 Starting development server with Docker PostgreSQL..."
	@echo "📚 API docs will be available at: http://localhost:8000/docs"
	@echo ""
	@# Ensure we're using Docker database configuration
	@if [ -f .env.docker ]; then \
		cp .env.docker .env; \
		echo "✅ Using Docker database configuration"; \
	fi
	@# Check if Docker PostgreSQL is running
	@if ! docker ps | grep -q trackwise_postgres; then \
		echo "⚠️  Docker PostgreSQL is not running!"; \
		echo "Run 'make docker-up' first"; \
		exit 1; \
	fi
	@echo "🚀 Starting server..."
	DATABASE_URL="postgresql://trackwise:trackwise_dev@localhost:5432/trackwise" .venv/bin/uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run development server with local database
run-local:
	@echo "💻 Starting development server with local PostgreSQL..."
	@echo "📚 API docs will be available at: http://localhost:8000/docs"
	@echo ""
	@# Ensure we're using local database configuration
	@if [ -f .env.local ]; then \
		cp .env.local .env; \
		echo "✅ Using local database configuration"; \
	fi
	@echo "🚀 Starting server..."
	.venv/bin/uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run tests
test:
	@echo "🧪 Running tests..."
	.venv/bin/pytest app/tests/ -v --cov=app --cov-report=term-missing

# Test all API endpoints
test-api:
	@echo "🧪 Testing all API endpoints..."
	@echo "📋 Make sure the server is running: make run"
	@echo ""
	PYTHONPATH=. .venv/bin/python scripts/test_api.py

# Create database if it doesn't exist
db-create:
	@echo "🗄️  Creating database if it doesn't exist..."
	PYTHONPATH=. .venv/bin/python scripts/create_db.py

# Create new migration
migrate:
	@echo "🔄 Creating new migration..."
	@read -p "Enter migration message: " message; \
	.venv/bin/alembic revision --autogenerate -m "$$message"

# Apply migrations
db-upgrade:
	@echo "⬆️  Applying database migrations..."
	.venv/bin/alembic upgrade head

# Rollback migration
db-downgrade:
	@echo "⬇️  Rolling back last migration..."
	.venv/bin/alembic downgrade -1

# Format code
format:
	@echo "🎨 Formatting code with black..."
	.venv/bin/black app/

# Lint code
lint:
	@echo "🔍 Running linting checks..."
	.venv/bin/flake8 app/
	.venv/bin/mypy app/

# Clean generated files
clean:
	@echo "🧹 Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete
	@echo "✅ Cleanup complete!"

# Docker commands
docker-up:
	@echo "🐳 Starting Docker containers..."
	docker-compose up -d
	@echo ""
	@echo "⏳ Waiting for PostgreSQL to be ready..."
	@sleep 5
	@echo "✅ Docker containers started!"
	@echo ""
	@echo "PostgreSQL: localhost:5432"
	@echo "Redis: localhost:6379"
	@echo ""
	@echo "Run 'make db-upgrade' if this is first time setup"

docker-down:
	@echo "🛑 Stopping Docker containers..."
	docker-compose down
	@echo "✅ Docker containers stopped!"

docker-status:
	@echo "📊 Docker containers status:"
	@docker-compose ps
	@echo ""
	@echo "Database info:"
	@docker exec trackwise_postgres psql -U trackwise -d trackwise -c "SELECT 'Users in database:' as info, COUNT(*) as count FROM users;" 2>/dev/null || echo "Database not ready or tables not created"

docker-db:
	@echo "🔍 Connecting to Docker PostgreSQL..."
	@echo "Type '\q' to exit"
	@echo ""
	docker exec -it trackwise_postgres psql -U trackwise -d trackwise