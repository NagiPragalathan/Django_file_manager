
python manage.py makemigrations
python manage.py migrate --no-input

gunicorn QuizApp.wsgi:application --bind 0.0.0.0:8000

unlink /etc/nginx/sites-enabled/default

nginx -g 'daemon off;'