from taskiq import TaskiqMiddleware


class StartShutdownMiddleware(TaskiqMiddleware):
    async def startup(self) -> None:
        from common.services.playwright import BaseRailwayTicketServiceParser

        BaseRailwayTicketServiceParser()

    async def shutdown(self) -> None:
        from common.services.playwright import BaseRailwayTicketServiceParser

        parser = BaseRailwayTicketServiceParser()
        await parser.stop_playwright_browser()
