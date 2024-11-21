import logging

from taskiq import TaskiqMiddleware

logger = logging.getLogger(__name__)


async def startup_playwright_browser() -> None:
    from common.services.playwright import BaseRailwayTicketServiceParser

    BaseRailwayTicketServiceParser()


async def shutdown_playwright_browser() -> None:
    from common.services.playwright import BaseRailwayTicketServiceParser

    parser = BaseRailwayTicketServiceParser()
    await parser.stop_playwright_browser()


class StartShutdownMiddleware(TaskiqMiddleware):
    async def startup(self) -> None:
        logger.info('The worker startup event has been started')
        await startup_playwright_browser()
        logger.info('The worker startup event successfully completed')

    async def shutdown(self) -> None:
        logger.info('The worker shutdown event has been started')
        await shutdown_playwright_browser()
        logger.info('The worker shutdown event successfully completed')
