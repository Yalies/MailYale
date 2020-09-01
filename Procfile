web: gunicorn app:app
beat: celery -A app.celery beat
worker: celery -A app.celery worker
