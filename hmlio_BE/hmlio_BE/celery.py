import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULES", "hmlio_BE.settings")

app = Celery("hmlio_BE")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks
