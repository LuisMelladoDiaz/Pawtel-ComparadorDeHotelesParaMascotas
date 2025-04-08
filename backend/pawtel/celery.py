import os

from celery import Celery

# Set the environment variable so Django uses the correct settings file
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pawtel.settings")

app = Celery("pawtel")

# Load Celery configuration from settings.py using the CELERY namespace
app.config_from_object("django.conf:settings", namespace="CELERY")

# Automatically discover tasks in installed apps
app.autodiscover_tasks()
