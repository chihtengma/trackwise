#!/bin/bash

# TrackWise API Test Runner
# This script runs comprehensive API tests

echo "================================"
echo "TrackWise API Test Suite"
echo "================================"
echo ""

cd ..

# Check if server is running
if ! curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "⚠️  Backend server is not running!"
    echo "Please start the server first with: make run"
    echo ""
    read -p "Would you like to start the server in the background? (y/n): " start_server

    if [ "$start_server" = "y" ]; then
        echo "Starting server in background..."
        source .venv/bin/activate
        nohup uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 > server.log 2>&1 &
        SERVER_PID=$!
        echo "Server started with PID: $SERVER_PID"
        echo "Waiting for server to be ready..."
        sleep 5
    else
        exit 1
    fi
fi

echo "Select test type:"
echo "1) Unit tests (pytest)"
echo "2) API integration tests"
echo "3) Full test suite (both)"
echo ""

read -p "Enter your choice (1-3): " choice

case $choice in
    1)
        echo "Running unit tests with pytest..."
        source .venv/bin/activate
        pytest app/tests/ -v --cov=app --cov-report=html
        echo ""
        echo "Coverage report available at: htmlcov/index.html"
        ;;

    2)
        echo "Running API integration tests..."
        python scripts/test_api.py

        if [ $? -eq 0 ]; then
            echo "✅ All API tests passed!"
        else
            echo "❌ Some API tests failed"
        fi
        ;;

    3)
        echo "Running full test suite..."
        echo ""
        echo "--- Unit Tests ---"
        source .venv/bin/activate
        pytest app/tests/ -v --cov=app --cov-report=html

        echo ""
        echo "--- API Integration Tests ---"
        python scripts/test_api.py

        echo ""
        echo "✅ Full test suite complete!"
        echo "Coverage report: htmlcov/index.html"
        ;;

    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac

# Clean up if we started the server
if [ ! -z "$SERVER_PID" ]; then
    echo ""
    echo "Stopping test server (PID: $SERVER_PID)..."
    kill $SERVER_PID 2>/dev/null
fi

echo ""
echo "Testing complete!"