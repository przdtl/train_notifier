import taskiq_aiogram

from taskiq import TaskiqScheduler

from taskiq_redis import RedisAsyncResultBackend, RedisScheduleSource, ListQueueBroker

from common.config import settings
from common.middlewares import StartShutdownMiddleware


broker = (
    ListQueueBroker(settings.TASKIQ_CONF.BROKER_URL)
    .with_result_backend(RedisAsyncResultBackend(settings.TASKIQ_CONF.BACKEND_URL))
    .with_middlewares(StartShutdownMiddleware())
)

redis_scheduler_source = RedisScheduleSource(settings.TASKIQ_CONF.SCHEDULE_SOURCE_URL)

scheduler = TaskiqScheduler(broker, sources=[redis_scheduler_source])

taskiq_aiogram.init(
    broker,
    "common.loader:dp",
    "common.loader:bot",
)
