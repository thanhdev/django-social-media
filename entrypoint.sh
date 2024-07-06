#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py migrate
npx tailwindcss -i ./static/src/input.css -o ./static/src/output.css
python manage.py collectstatic --no-input

exec "$@"
