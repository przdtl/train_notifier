from aiohttp import web

from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from common.loader import bot, dp
from common.config import settings
from common.logging import setup_logging

from routes.routers import router as routes_router
from trains.routers import router as trains_router
from tickets.routers import router as tickets_router
from scheduler.routers import router as scheduler_router

import bootstrap

dp.include_routers(
    routes_router,
    trains_router,
    scheduler_router,
    tickets_router,
)


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
    setup_logging()
    webhook_bot_run()


if __name__ == "__main__":
    main()
