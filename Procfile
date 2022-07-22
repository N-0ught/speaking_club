web: daphne speaking_club.asgi:application --port $PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker channel_layers --settings=speaking_club.settings -v2