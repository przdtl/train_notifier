from abc import abstractmethod, ABCMeta

from playwright.async_api import async_playwright

from common.utils import run_async


class BaseRailwayTicketServiceParser:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            run_async(cls.__run_playwright_browser)
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @classmethod
    async def __run_playwright_browser(cls) -> None:
        cls.__playwright = await async_playwright().start() if not cls.__instance else cls.__playwright
        cls.__browser = await cls.__playwright.chromium.launch(headless=False) if not cls.__instance else cls.__browser

    @classmethod
    async def stop_playwright_browser(cls) -> None:
        await cls.__browser.close()
        await cls.__playwright.stop()


class AbstractTrainParser(BaseRailwayTicketServiceParser, metaclass=ABCMeta):
    @abstractmethod
    def parse(self):
        ...


class AbstractTicketsParser(BaseRailwayTicketServiceParser, metaclass=ABCMeta):
    @abstractmethod
    def parse(self):
        ...


class BaseRailwayTicketService:
    pass


class TutuService(BaseRailwayTicketService):
    pass


class RZDService(BaseRailwayTicketService):
    pass
