#!/bin/bash
set -e

echo "Running database migrations..."
alembic upgrade head || echo "Migrations skipped (DB might not be ready yet)"

echo "Starting backend server..."
exec uvicorn app.main:app --host 0.0.0.0 --port $PORT
