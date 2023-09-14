web: gunicorn portfolio:wsgi
web: daphne core.core.asgi:application --port $PORT --bind 0.0.0.0 -v2
chatworker: python manage.py runworker --settings=core.core.settings -v2


