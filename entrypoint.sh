#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Function to wait for the database to be ready
function waitForDB() {
    echo "Waiting for database..."
    while ! nc -z $DB_HOST $DB_PORT; do
        sleep 0.1
    done
    echo "Database started"
}

# Wait for database to start up
waitForDB

# Run Django database migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start Gunicorn server
echo "Starting Gunicorn server..."
exec gunicorn statewideplanCWB.wsgi:application --bind 0.0.0.0:8000
