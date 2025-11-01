.PHONY: help install run test clean migrate db-upgrade db-downgrade format lint db-create

# Default target - show help
help:
	@echo "📋 TrackWise Transit AI - Available Commands"
	@echo "========================================"
	@echo ""
	@echo "  make install        - 🔧 Set up virtual environment and install dependencies"
	@echo "  make run           - 🚀 Run the development server"
	@echo "  make test          - 🧪 Run tests with pytest"
	@echo "  make db-create     - 🗄️  Create database if it doesn't exist"
	@echo "  make migrate       - 🔄 Create a new database migration"
	@echo "  make db-upgrade    - ⬆️  Apply database migrations"
	@echo "  make db-downgrade  - ⬇️  Rollback last migration"
	@echo "  make format        - 🎨 Format code with black"
	@echo "  make lint          - 🔍 Run linting checks"
	@echo "  make clean         - 🧹 Remove generated files and caches"
	@echo ""
	@echo "First time setup: make install"
	@echo "Start coding:     make run"
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

# Run development server
run:
	@echo "🚀 Starting development server..."
	@echo "📚 API docs will be available at: http://localhost:8000/docs"
	@echo ""
	.venv/bin/uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run tests
test:
	@echo "🧪 Running tests..."
	.venv/bin/pytest tests/ -v --cov=app --cov-report=term-missing

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
	.venv/bin/black app/ tests/

# Lint code
lint:
	@echo "🔍 Running linting checks..."
	.venv/bin/flake8 app/ tests/
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