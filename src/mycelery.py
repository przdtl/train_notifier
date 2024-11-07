from celery import Celery

from config import settings

app = Celery(
    'train_notifier',
    broker=settings.CELERY_CONF.BROKER_URL,
    backend=settings.CELERY_CONF.BACKEND_URL,
    include=['tasks.selenium']
)
