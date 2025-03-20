from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Définir le module Django par défaut pour le programme Celery.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
app = Celery('dataviewer-queue')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))