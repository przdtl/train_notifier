"""
Модуль содержит логику, включаемую непосредственно во время запуска приложения и при его завершении

event, срабатываемый при запуске приложения:
    - setup_app

event, срабатываемый при завершении работы приложения:
    - shutdown_app

"""

import logging

from aiogram import Bot

from common.loader import dp
from common.config import settings
from common.broker import broker

logger = logging.getLogger(__name__)


async def setup_taskiq() -> None:
    if not broker.is_worker_process:
        await broker.startup()


async def shutdown_taskiq() -> None:
    if not broker.is_worker_process:
        await broker.shutdown()


async def setup_telegram_webhook(bot: Bot) -> None:
    await bot.set_webhook('{}{}'.format(
        settings.TELEGRAM_CONF.WEBHOOK_CONF.BASE_WEBHOOK_URL,
        settings.TELEGRAM_CONF.WEBHOOK_CONF.WEBHOOK_PATH,
    ))


async def shutdown_telegram_webhook(bot: Bot) -> None:
    await bot.delete_webhook()


@dp.startup()
async def setup_app(bot: Bot):
    logger.info('The app startup event has been started')
    await setup_taskiq()
    await setup_telegram_webhook(bot)
    logger.info('The app startup event successfully completed ')


@dp.shutdown()
async def shutdown_app(bot: Bot):
    logger.info('The app shutdown event has been started')
    await shutdown_taskiq()
    await shutdown_telegram_webhook(bot)
    logger.info('The app shutdown event successfully completed ')
