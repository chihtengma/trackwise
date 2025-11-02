#!/usr/bin/env python3
"""
API test script for TrackWise Transit AI Assistant.

This script tests all API endpoints and provides detailed output.
Run this while the server is running: make run

Usage:
    python scripts/test_api.py
"""

import json
import sys
from datetime import datetime
from typing import Optional

import httpx

# API base URL
BASE_URL = "http://localhost:8000"
API_V1_URL = f"{BASE_URL}/api/v1"

# Test results tracking
passed_tests = 0
failed_tests = 0
test_results = []


def print_header(text: str):
    """Print a formatted header."""
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80)


def print_test(name: str, status: str, details: str = ""):
    """Print test result with formatting."""
    icon = "✅" if status == "PASS" else "❌"
    print(f"\n{icon} {name}")
    if details:
        print(f"   {details}")
    test_results.append((name, status, details))


def test_endpoint(
    method: str,
    url: str,
    expected_status: int,
    headers: Optional[dict] = None,
    data: Optional[dict] = None,
    description: str = "",
) -> Optional[dict]:
    """
    Test an API endpoint.

    Args:
        method: HTTP method (GET, POST, PATCH, DELETE)
        url: Full URL to test
        expected_status: Expected HTTP status code
        headers: Optional headers to include
        data: Optional request body
        description: Test description

    Returns:
        Response JSON if successful, None otherwise
    """
    global passed_tests, failed_tests

    try:
        # Make request
        if method == "GET":
            response = httpx.get(url, headers=headers, timeout=10.0)
        elif method == "POST":
            if (
                headers
                and headers.get("Content-Type") == "application/x-www-form-urlencoded"
            ):
                response = httpx.post(url, headers=headers, data=data, timeout=10.0)
            else:
                response = httpx.post(url, headers=headers, json=data, timeout=10.0)
        elif method == "PATCH":
            response = httpx.patch(url, headers=headers, json=data, timeout=10.0)
        elif method == "DELETE":
            response = httpx.delete(url, headers=headers, timeout=10.0)
        else:
            print_test(f"{method} {url}", "FAIL", f"Unsupported method: {method}")
            failed_tests += 1
            return None

        # Check status code
        if response.status_code == expected_status:
            passed_tests += 1
            if response.content:
                try:
                    result = response.json()
                    print_test(
                        description or f"{method} {url}",
                        "PASS",
                        f"Status: {response.status_code}",
                    )
                    return result
                except json.JSONDecodeError:
                    print_test(
                        description or f"{method} {url}",
                        "PASS",
                        f"Status: {response.status_code} (No JSON)",
                    )
                    return None
            else:
                print_test(
                    description or f"{method} {url}",
                    "PASS",
                    f"Status: {response.status_code}",
                )
                return None
        else:
            failed_tests += 1
            error_detail = (
                f"Status: {response.status_code} (expected {expected_status})"
            )
            if response.content:
                try:
                    error_json = response.json()
                    if "detail" in error_json:
                        error_detail += f" - {error_json['detail']}"
                except json.JSONDecodeError:
                    error_detail += f" - {response.text[:100]}"
            print_test(description or f"{method} {url}", "FAIL", error_detail)
            return None

    except httpx.ConnectError:
        failed_tests += 1
        print_test(
            f"{method} {url}",
            "FAIL",
            "Connection error - Is the server running? Try: make run",
        )
        return None
    except Exception as e:
        failed_tests += 1
        print_test(f"{method} {url}", "FAIL", f"Unexpected error: {str(e)}")
        return None


def main():
    """Run all API tests."""
    global passed_tests, failed_tests

    print_header("TrackWise Transit AI Assistant - API Test Suite")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Testing API at: {BASE_URL}")

    # ==================== General Endpoints ====================
    print_header("General Endpoints")

    test_endpoint("GET", f"{BASE_URL}/", 200, description="Root endpoint")
    test_endpoint("GET", f"{BASE_URL}/health", 200, description="Health check")
    test_endpoint(
        "GET", f"{BASE_URL}/docs", 200, description="API documentation (Swagger UI)"
    )
    test_endpoint(
        "GET", f"{BASE_URL}/openapi.json", 200, description="OpenAPI JSON schema"
    )

    # ==================== Authentication Endpoints ====================
    print_header("Authentication Endpoints")

    # Register first user
    register_data = {
        "email": "testuser@example.com",
        "username": "testuser",
        "password": "TestPass123!",
        "full_name": "Test User",
    }
    test_endpoint(
        "POST",
        f"{API_V1_URL}/auth/register",
        201,
        data=register_data,
        description="Register new user",
    )

    # Try to register duplicate user (should fail)
    test_endpoint(
        "POST",
        f"{API_V1_URL}/auth/register",
        409,
        data=register_data,
        description="Try to register duplicate user (should fail)",
    )

    # Login
    login_data = {
        "username": "testuser@example.com",  # Note: use email as username
        "password": "TestPass123!",
    }
    login_headers = {"Content-Type": "application/x-www-form-urlencoded"}
    login_response = test_endpoint(
        "POST",
        f"{API_V1_URL}/auth/login",
        200,
        headers=login_headers,
        data=login_data,
        description="Login with valid credentials",
    )

    # Get access token
    access_token = None
    if login_response:
        access_token = login_response.get("access_token")
        print(
            f"\n   🔑 Access token received: {access_token[:50]}..."
            if access_token
            else ""
        )

    # Try to login with invalid credentials
    test_endpoint(
        "POST",
        f"{API_V1_URL}/auth/login",
        401,
        headers=login_headers,
        data={"username": "testuser@example.com", "password": "WrongPassword"},
        description="Login with invalid password (should fail)",
    )

    # ==================== User Endpoints ====================
    print_header("User Endpoints")

    if not access_token:
        print("\n⚠️  Skipping authenticated endpoints - no access token")
    else:
        auth_headers = {"Authorization": f"Bearer {access_token}"}

        # Get current user
        current_user = test_endpoint(
            "GET",
            f"{API_V1_URL}/users/me",
            200,
            headers=auth_headers,
            description="Get current user profile",
        )

        # Get user by ID
        if current_user and "id" in current_user:
            user_id = current_user["id"]
            test_endpoint(
                "GET",
                f"{API_V1_URL}/users/{user_id}",
                200,
                headers=auth_headers,
                description=f"Get user by ID ({user_id})",
            )

            # Try to access another user's profile (should fail)
            test_endpoint(
                "GET",
                f"{API_V1_URL}/users/999999",
                404,
                headers=auth_headers,
                description="Try to get non-existent user (should fail)",
            )

            # Update user
            update_data = {"full_name": "Updated Test User"}
            test_endpoint(
                "PATCH",
                f"{API_V1_URL}/users/{user_id}",
                200,
                headers=auth_headers,
                data=update_data,
                description="Update user profile",
            )

        # Try to access without token
        test_endpoint(
            "GET",
            f"{API_V1_URL}/users/me",
            401,
            description="Get current user without token (should fail)",
        )

        # Try to access with invalid token
        test_endpoint(
            "GET",
            f"{API_V1_URL}/users/me",
            401,
            headers={"Authorization": "Bearer invalid_token_here"},
            description="Get current user with invalid token (should fail)",
        )

    # ==================== Admin Endpoints ====================
    print_header("Admin Endpoints (Superuser Only)")

    # Create admin user
    admin_register_data = {
        "email": "admin@example.com",
        "username": "admin",
        "password": "AdminPass123!",
        "full_name": "Admin User",
    }

    # Register admin (as normal user first)
    test_endpoint(
        "POST",
        f"{API_V1_URL}/auth/register",
        201,
        data=admin_register_data,
        description="Register admin user",
    )

    # Login as admin
    admin_login_data = {
        "username": "admin@example.com",
        "password": "AdminPass123!",
    }
    admin_login_response = test_endpoint(
        "POST",
        f"{API_V1_URL}/auth/login",
        200,
        headers=login_headers,
        data=admin_login_data,
        description="Login as admin",
    )

    # Note: Admin endpoints will fail because user is not marked as superuser
    # In production, you'd need to manually mark users as superuser in the database
    if admin_login_response and admin_login_response.get("access_token"):
        admin_token = admin_login_response.get("access_token")
        admin_auth_headers = {"Authorization": f"Bearer {admin_token}"}

        # Try to list all users (will fail if not superuser)
        test_endpoint(
            "GET",
            f"{API_V1_URL}/users/?skip=0&limit=10",
            403,
            headers=admin_auth_headers,
            description="List all users (requires superuser)",
        )

        # Try to delete user (will fail if not superuser)
        if current_user and "id" in current_user:
            user_id = current_user["id"]
            test_endpoint(
                "DELETE",
                f"{API_V1_URL}/users/{user_id}",
                403,
                headers=admin_auth_headers,
                description="Delete user (requires superuser)",
            )

    # ==================== Summary ====================
    print_header("Test Summary")
    total_tests = passed_tests + failed_tests
    success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0

    print(f"\n📊 Total Tests: {total_tests}")
    print(f"✅ Passed: {passed_tests}")
    print(f"❌ Failed: {failed_tests}")
    print(f"📈 Success Rate: {success_rate:.1f}%")

    # Print failed tests if any
    failed_results = [r for r in test_results if r[1] == "FAIL"]
    if failed_results:
        print("\n❌ Failed Tests:")
        for name, status, details in failed_results:
            print(f"   • {name}: {details}")

    # Return exit code
    exit_code = 0 if failed_tests == 0 else 1
    return exit_code


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
