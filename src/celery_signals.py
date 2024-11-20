import asyncio

from celery.signals import worker_shutting_down, worker_init


async def async_worker_init() -> None:
    from common.services.playwright import BaseRailwayTicketServiceParser
    BaseRailwayTicketServiceParser()


async def async_worker_shutting_down() -> None:
    from common.services.playwright import BaseRailwayTicketServiceParser

    parser = BaseRailwayTicketServiceParser()
    asyncio.run(parser.stop_playwright_browser())


@worker_init.connect
def worker_on_init(*args, **kwargs) -> None:
    asyncio.run(async_worker_init())


@worker_shutting_down.connect
def worker_on_shutdown(*args, **kwargs) -> None:
    asyncio.run(async_worker_shutting_down())
