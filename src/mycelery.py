from celery import Celery
from celery.schedules import crontab

from config import settings

app = Celery(
    'train_notifier',
    broker=settings.CELERY_CONF.BROKER_URL,
    backend=settings.CELERY_CONF.BACKEND_URL,
)
app.autodiscover_tasks(['trains', 'tickets', 'waiting', 'schedule'])

app.conf.update({
    'beat_schedule': {},
    'timezone': 'UTC',
})
