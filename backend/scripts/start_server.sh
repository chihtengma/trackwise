#!/bin/bash

# TrackWise Backend Server Starter
# This script provides an interactive way to start the backend with either Docker or local database

echo "================================"
echo "TrackWise Backend Server"
echo "================================"
echo ""

# Function to check if service is running
check_service() {
    local service=$1
    local port=$2
    if nc -z localhost $port 2>/dev/null; then
        echo "✅ $service is running on port $port"
        return 0
    else
        echo "❌ $service is not running on port $port"
        return 1
    fi
}

# Check which services are available
echo "Checking available services..."
echo "------------------------------"

LOCAL_PG=false
DOCKER_PG=false

# Check PostgreSQL
if pgrep -f "postgres.*postgresql@16" > /dev/null; then
    LOCAL_PG=true
    echo "✅ Local PostgreSQL (Homebrew) is running"
else
    echo "⚠️  Local PostgreSQL is not running"
fi

if docker ps | grep -q "trackwise.*postgres"; then
    DOCKER_PG=true
    echo "✅ Docker PostgreSQL is running"
else
    echo "⚠️  Docker PostgreSQL is not running"
fi

# Check Redis
check_service "Redis" 6379

echo ""
echo "Select database environment:"
echo "=========================="
echo "1) Docker (Recommended - uses Docker PostgreSQL)"
echo "2) Local (uses Homebrew PostgreSQL)"
echo "3) Custom (use existing .env file)"
echo ""

read -p "Enter your choice (1-3): " choice

case $choice in
    1)
        if [ "$DOCKER_PG" = false ]; then
            echo "⚠️  Docker PostgreSQL is not running!"
            echo ""
            echo "Would you like to start Docker containers now?"
            read -p "Start Docker containers? (y/n): " start_docker
            if [ "$start_docker" = "y" ]; then
                echo "Starting Docker containers..."
                cd .. && docker-compose up -d postgres redis
                echo "Waiting for services to be ready..."
                sleep 5
                cd scripts
            else
                echo "Please run: make docker-up"
                exit 1
            fi
        fi
        ENV_FILE="../.env.docker"
        echo "Using DOCKER environment"
        ;;
    2)
        if [ "$LOCAL_PG" = false ]; then
            echo "⚠️  Local PostgreSQL is not running!"
            echo "Start it with: brew services start postgresql@16"
            read -p "Continue anyway? (y/n): " cont
            if [ "$cont" != "y" ]; then
                exit 1
            fi
        fi
        ENV_FILE="../.env.local"
        echo "Using LOCAL environment"
        ;;
    3)
        ENV_FILE="../.env"
        echo "Using CUSTOM environment (.env)"
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac

# Copy selected environment file
cd ..
if [ "$ENV_FILE" != ".env" ] && [ -f "${ENV_FILE#../}" ]; then
    echo ""
    echo "Copying ${ENV_FILE#../} to .env..."
    cp "${ENV_FILE#../}" .env
fi

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

# Activate virtual environment
if [ -d ".venv" ]; then
    echo "Activating virtual environment..."
    source .venv/bin/activate
else
    echo "No virtual environment found. Please run: make install"
    exit 1
fi

# Get IP address for mobile testing
IP_ADDRESS=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | head -n 1 | awk '{print $2}')

echo ""
echo "================================"
echo "Starting TrackWise Backend"
echo "================================"
echo "Environment: ${ENV_FILE#../}"
echo ""
echo "Access points:"
echo "- Local: http://localhost:8000"
echo "- Network: http://$IP_ADDRESS:8000"
echo "- API Docs: http://localhost:8000/docs"
echo ""
echo "For Flutter app, update frontend/.env:"
echo "API_BASE_URL=http://$IP_ADDRESS:8000"
echo "================================"
echo ""

# Start the backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000