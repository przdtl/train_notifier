import sys
import logging

from aiohttp import web

from aiogram import Bot
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from common.loader import bot, dp
from common.config import settings
from common.broker import broker


@dp.startup()
async def setup_taskiq(bot: Bot, *_args, **_kwargs):
    await bot.set_webhook('{}{}'.format(
        settings.TELEGRAM_CONF.WEBHOOK_CONF.BASE_WEBHOOK_URL,
        settings.TELEGRAM_CONF.WEBHOOK_CONF.WEBHOOK_PATH,
    ))
    if not broker.is_worker_process:
        logging.info("Setting up taskiq")
        await broker.startup()


@dp.shutdown()
async def shutdown_taskiq(bot: Bot, *_args, **_kwargs):
    await bot.delete_webhook()
    if not broker.is_worker_process:
        logging.info("Shutting down taskiq")
        await broker.shutdown()


def webhook_bot_run() -> None:
    app = web.Application()

    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    )
    webhook_requests_handler.register(
        app,
        path=settings.TELEGRAM_CONF.WEBHOOK_CONF.WEBHOOK_PATH,
    )

    setup_application(app, dp, bot=bot)
    web.run_app(
        app=app,
        host=settings.TELEGRAM_CONF.WEBHOOK_CONF.WEB_SERVER_HOST,
        port=settings.TELEGRAM_CONF.WEBHOOK_CONF.WEB_SERVER_PORT,
    )


def main() -> None:
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    webhook_bot_run()


if __name__ == "__main__":
    main()
