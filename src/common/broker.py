import taskiq_aiogram

from taskiq_redis import RedisAsyncResultBackend
from taskiq_aio_pika import AioPikaBroker

from common.config import settings

broker = AioPikaBroker(
    settings.TASKIQ_CONF.BROKER_URL
).with_result_backend(RedisAsyncResultBackend(
    settings.TASKIQ_CONF.BACKEND_URL
))

taskiq_aiogram.init(
    broker,
    "common.loader:dp",
    "common.loader:bot",
)
