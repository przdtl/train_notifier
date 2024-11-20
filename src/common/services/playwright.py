import asyncio

from playwright.async_api import async_playwright

from common.exceptions import BrowserNotInitializedError


class BaseRailwayTicketServiceParser:
    _playwright = None
    _browser = None

    def __new__(cls, *args, **kwargs):
        if cls._playwright is None or cls._browser is None:
            asyncio.create_task(cls._run_playwright_browser())

        return super().__new__(cls, *args, **kwargs)

    @classmethod
    async def _run_playwright_browser(cls) -> None:
        cls._playwright = await async_playwright().start() if not cls._playwright else cls._playwright
        cls._browser = await cls._playwright.chromium.launch(headless=True, args=["--no-sandbox"]) if not cls._browser else cls._browser

    @classmethod
    async def stop_playwright_browser(cls) -> None:
        if cls._playwright is None or cls._browser is None:
            raise BrowserNotInitializedError

        await cls._browser.close()
        await cls._playwright.stop()

    async def _open_page(self, url: str) -> None:
        if self._playwright is None or self._browser is None:
            raise BrowserNotInitializedError

        self._page = await self._browser.new_page()
        await self._page.goto(url)
