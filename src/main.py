import sys
import logging

from aiohttp import web

from aiogram import Bot
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from utils.loader import bot, dp
from utils.config import settings

from utils.db import db


async def on_startup(bot: Bot) -> None:
    await bot.set_webhook('{}{}'.format(
        settings.TELEGRAM_CONF.WEBHOOK_CONF.BASE_WEBHOOK_URL,
        settings.TELEGRAM_CONF.WEBHOOK_CONF.WEBHOOK_PATH,
    ))


async def on_shutdown(bot: Bot) -> None:
    await bot.delete_webhook()


def webhook_bot_run() -> None:
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

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
