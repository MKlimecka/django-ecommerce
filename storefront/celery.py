import os
from django.conf import settings
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'storefront.settings.dev')

celery = Celery('storefront', broker=settings.CELERY_BROKER_URL)
celery.config_from_object('django.conf:settings', namespace='CELERY')
celery.autodiscover_tasks()