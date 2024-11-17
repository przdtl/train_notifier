from celery.signals import worker_shutting_down, worker_init

from common.utils import run_async


@worker_init.connect
def worker_on_init(*args, **kwargs) -> None:
    from common.services.playwright import BaseRailwayTicketServiceParser

    BaseRailwayTicketServiceParser()


@worker_shutting_down.connect
def worker_on_shutdown(*args, **kwargs) -> None:
    from common.services.playwright import BaseRailwayTicketServiceParser

    parser = BaseRailwayTicketServiceParser()
    run_async(parser.stop_playwright_browser)
