#!/bin/bash

# TrackWise Database Setup Script
# This script helps set up either Docker or local PostgreSQL database

echo "================================"
echo "TrackWise Database Setup"
echo "================================"
echo ""

echo "Select database setup option:"
echo "1) Setup Docker PostgreSQL (Recommended)"
echo "2) Setup Local PostgreSQL (Homebrew)"
echo "3) Run migrations only (database already exists)"
echo ""

read -p "Enter your choice (1-3): " choice

cd ..

case $choice in
    1)
        echo "Setting up Docker PostgreSQL..."

        # Check if Docker is running
        if ! docker info > /dev/null 2>&1; then
            echo "❌ Docker is not running. Please start Docker Desktop."
            exit 1
        fi

        # Start Docker containers
        echo "Starting Docker containers..."
        docker-compose up -d postgres redis

        # Wait for PostgreSQL to be ready
        echo "Waiting for PostgreSQL to be ready..."
        sleep 5

        # Create database if it doesn't exist
        echo "Creating database..."
        docker exec -it trackwise-postgres psql -U trackwise -c "SELECT 1;" > /dev/null 2>&1
        if [ $? -eq 0 ]; then
            echo "✅ Database is ready"
        else
            echo "❌ Failed to connect to database"
            exit 1
        fi

        # Use Docker environment
        cp .env.docker .env
        export $(cat .env | grep -v '^#' | xargs)

        # Run migrations
        echo "Running migrations..."
        source .venv/bin/activate 2>/dev/null || source venv/bin/activate 2>/dev/null
        alembic upgrade head

        echo ""
        echo "✅ Docker PostgreSQL setup complete!"
        echo "Connection string: postgresql://trackwise:trackwise_dev@localhost:5432/trackwise"
        ;;

    2)
        echo "Setting up Local PostgreSQL..."

        # Check if PostgreSQL is installed
        if ! command -v psql &> /dev/null; then
            echo "PostgreSQL is not installed."
            echo "Install with: brew install postgresql@16"
            exit 1
        fi

        # Check if PostgreSQL is running
        if ! brew services list | grep "postgresql@16.*started" > /dev/null; then
            echo "PostgreSQL is not running."
            echo "Starting PostgreSQL..."
            brew services start postgresql@16
            sleep 3
        fi

        # Create database
        echo "Creating database 'trackwise'..."
        createdb trackwise 2>/dev/null || echo "Database might already exist"

        # Use local environment
        cp .env.local .env
        export $(cat .env | grep -v '^#' | xargs)

        # Run migrations
        echo "Running migrations..."
        source .venv/bin/activate 2>/dev/null || source venv/bin/activate 2>/dev/null
        alembic upgrade head

        echo ""
        echo "✅ Local PostgreSQL setup complete!"
        echo "Connection string: postgresql://$(whoami):@localhost:5432/trackwise"
        ;;

    3)
        echo "Running migrations only..."

        # Load environment
        export $(cat .env | grep -v '^#' | xargs)

        # Run migrations
        source .venv/bin/activate 2>/dev/null || source venv/bin/activate 2>/dev/null
        alembic upgrade head

        if [ $? -eq 0 ]; then
            echo "✅ Migrations completed successfully"
        else
            echo "❌ Migration failed. Check your DATABASE_URL in .env"
            exit 1
        fi
        ;;

    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac

echo ""
echo "Database setup complete!"
echo "You can now start the server with: make run"