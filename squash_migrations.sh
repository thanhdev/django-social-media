python manage.py migrate home zero
rm -r home/migrations/000*
python manage.py makemigrations home
python manage.py migrate home
