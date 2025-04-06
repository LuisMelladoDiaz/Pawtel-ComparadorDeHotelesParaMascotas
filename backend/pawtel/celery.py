import os

from celery import Celery

# Establece la variable de entorno para que Django use el archivo de settings correcto
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pawtel.settings")

app = Celery("pawtel")

# Carga la configuración de Celery desde el settings.py usando el namespace CELERY
app.config_from_object("django.conf:settings", namespace="CELERY")

# Descubre automáticamente las tareas en las apps instaladas
app.autodiscover_tasks()
