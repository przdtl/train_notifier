from aiogram import Bot

from common.loader import dp
from common.config import settings
from common.broker import broker


async def setup_taskiq() -> None:
    if not broker.is_worker_process:
        await broker.startup()


async def shutdown_taskiq() -> None:
    if not broker.is_worker_process:
        await broker.shutdown()


async def telegram_webhook_init(bot: Bot) -> None:
    await bot.set_webhook('{}{}'.format(
        settings.TELEGRAM_CONF.WEBHOOK_CONF.BASE_WEBHOOK_URL,
        settings.TELEGRAM_CONF.WEBHOOK_CONF.WEBHOOK_PATH,
    ))


async def telegram_webhook_shutdown(bot: Bot) -> None:
    await bot.delete_webhook()


@dp.startup()
async def setup_app(bot: Bot):
    await setup_taskiq()
    await telegram_webhook_init(bot)


@dp.shutdown()
async def shutdown_app(bot: Bot):
    await shutdown_taskiq()
    await telegram_webhook_shutdown(bot)
