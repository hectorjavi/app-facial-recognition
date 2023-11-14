#!/bin/bash

echo "Waiting for postgres..."

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 0.1
done

echo "PostgreSQL started"

echo "Appling database migrations..."

if [ $PRODUCTION -eq 1 ]; then
    echo "Running in Production Mode"
    python manage.py makemigrations --settings=core.settings.prod
    python manage.py migrate --settings=core.settings.prod
    python manage.py collectstatic --no-input --settings=core.settings.prod
    python manage.py runserver 0.0.0.0:$PORT --settings=core.settings.prod
    # gunicorn -w 1 --env DJANGO_SETTINGS_MODULE=core.settings.prod core.wsgi:application --bind 0.0.0.0:$PORT
else
    echo "Running in Developer Mode"
    python manage.py makemigrations
    python manage.py migrate
fi

exec "$@"
