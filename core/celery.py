# core/celery.py
import os
from celery import Celery

# Establece el módulo de configuración de Django por defecto
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Crea la instancia de Celery
app = Celery('core')

# Carga la configuración desde settings.py (usando el prefijo CELERY_)
app.config_from_object('django.conf:settings', namespace='CELERY')

# Busca tareas automáticamente en las apps de Django
app.autodiscover_tasks()