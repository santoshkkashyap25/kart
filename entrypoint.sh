#!/bin/sh

# Apply database migrations
echo "Applying migrations..."
python manage.py migrate --noinput

# Seed database with dummy data
echo "Seeding data..."
python manage.py seed_data

# Create superuser if it doesn't exist
# We use environment variables: DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL, DJANGO_SUPERUSER_PASSWORD
if [ "$DJANGO_SUPERUSER_USERNAME" ]; then
    echo "Creating superuser..."
    python manage.py createsuperuser --noinput || echo "Superuser already exists."
fi

# Start server
echo "Starting server..."
python manage.py runserver 0.0.0.0:8000
