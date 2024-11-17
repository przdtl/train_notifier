from celery import Celery

from common.config import settings

app = Celery(
    'train_notifier',
    broker=settings.CELERY_CONF.BROKER_URL,
    backend=settings.CELERY_CONF.BACKEND_URL,
)
app.conf.broker_connection_retry_on_startup = True

import celery_signals

app.autodiscover_tasks(['trains', 'tickets', 'waiting', 'scheduler'])
