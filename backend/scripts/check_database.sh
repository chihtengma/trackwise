#!/bin/bash

# TrackWise Database Status Checker
# This script checks database connection and displays user information

echo "================================"
echo "TrackWise Database Status"
echo "================================"
echo ""

# Function to check PostgreSQL connection
check_postgres() {
    local db_url=$1
    local type=$2

    echo "Checking $type database..."

    # Parse DATABASE_URL
    if [[ $db_url =~ postgresql://([^:]+):([^@]*)@([^:]+):([^/]+)/(.+) ]]; then
        USER="${BASH_REMATCH[1]}"
        PASS="${BASH_REMATCH[2]}"
        HOST="${BASH_REMATCH[3]}"
        PORT="${BASH_REMATCH[4]}"
        DB="${BASH_REMATCH[5]}"

        # Test connection
        PGPASSWORD="$PASS" psql -h "$HOST" -p "$PORT" -U "$USER" -d "$DB" -c "SELECT COUNT(*) as user_count FROM users;" 2>/dev/null

        if [ $? -eq 0 ]; then
            echo "✅ $type database is accessible"

            # Get more details
            PGPASSWORD="$PASS" psql -h "$HOST" -p "$PORT" -U "$USER" -d "$DB" -c "
                SELECT
                    'Total Users: ' || COUNT(*) as metric,
                    '' as value
                FROM users
                UNION ALL
                SELECT
                    'Latest User: ' as metric,
                    email as value
                FROM users
                ORDER BY created_at DESC
                LIMIT 1;
            " 2>/dev/null

            return 0
        else
            echo "❌ Cannot connect to $type database"
            return 1
        fi
    else
        echo "❌ Invalid DATABASE_URL format"
        return 1
    fi
}

# Check which environment is being used
cd ..

if [ -f ".env" ]; then
    echo "Using configuration from .env"
    export $(cat .env | grep -v '^#' | xargs)
    check_postgres "$DATABASE_URL" "Current"
else
    echo "No .env file found. Checking both databases..."
    echo ""

    # Check Docker database
    if [ -f ".env.docker" ]; then
        echo "--- Docker Database ---"
        export $(cat .env.docker | grep -v '^#' | xargs)
        check_postgres "$DATABASE_URL" "Docker"
        echo ""
    fi

    # Check Local database
    if [ -f ".env.local" ]; then
        echo "--- Local Database ---"
        export $(cat .env.local | grep -v '^#' | xargs)
        check_postgres "$DATABASE_URL" "Local"
        echo ""
    fi
fi

# Check services status
echo ""
echo "================================"
echo "Service Status"
echo "================================"

# Docker services
if docker ps > /dev/null 2>&1; then
    echo ""
    echo "Docker Services:"
    docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep -E "(NAME|trackwise|redis)"
fi

# Local services
echo ""
echo "Local Services:"
if brew services list | grep "postgresql@16.*started" > /dev/null 2>&1; then
    echo "✅ PostgreSQL@16 (Homebrew) is running"
else
    echo "⚠️  PostgreSQL@16 (Homebrew) is stopped"
fi

if pgrep -f redis-server > /dev/null 2>&1; then
    echo "✅ Redis is running"
else
    echo "⚠️  Redis is not running"
fi

echo ""
echo "To switch databases, use: ./scripts/start_server.sh"