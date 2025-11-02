#!/usr/bin/env python3
"""
Create database if it doesn't exist.

This script reads the DATABASE_URL from config and creates the database
if it doesn't already exist.
"""
import re
import sys

try:
    import psycopg2
    from app.core.config import settings
except ImportError as e:
    print(f"❌ Error importing dependencies: {e}")
    sys.exit(1)


def main():
    """Create database if it doesn't exist."""
    url = settings.DATABASE_URL
    match = re.match(r"postgresql://([^:]+):([^@]+)@([^:]+):(\d+)/(.+)", url)

    if not match:
        print(f"❌ Could not parse DATABASE_URL: {url}")
        sys.exit(1)

    user, password, host, port, db_name = match.groups()

    try:
        # Connect to postgres database to create new database
        conn = psycopg2.connect(
            f"postgresql://{user}:{password}@{host}:{port}/postgres"
        )
        conn.autocommit = True
        cursor = conn.cursor()

        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
        exists = cursor.fetchone()

        if not exists:
            cursor.execute(f'CREATE DATABASE "{db_name}"')
            print(f"✅ Created database: {db_name}")
        else:
            print(f"✅ Database already exists: {db_name}")

        conn.close()
        sys.exit(0)

    except Exception as e:
        print(f"❌ Error creating database: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
