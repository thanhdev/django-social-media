npx tailwindcss -i ./static/src/input.css -o ./static/src/output.css
python manage.py collectstatic --noinput
python manage.py runserver 0.0.0.0:8000
