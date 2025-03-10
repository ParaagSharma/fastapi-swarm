#!/bin/sh

echo "Waiting for PostgreSQL to be ready..."

until /usr/lib/postgresql/15/bin/pg_isready -h db -U test -d fast_todo_app; do
  echo "Postgres is unavailable - sleeping"
  sleep 2
done

echo "Postgres is up - starting FastAPI"
exec uvicorn app.main:app --host 0.0.0.0 --reload --port 8011