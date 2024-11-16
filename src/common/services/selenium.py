from typing import TypeVar, Type, Generic

from pydantic import HttpUrl

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from config import settings


T = TypeVar('T', bound='TutuParser')


class TutuParser:
    def __init__(self, options: Options, remote_url: str | None = None) -> None:
        self.options = options

        if remote_url:
            self.__driver = webdriver.Remote(
                remote_url,
                options=self.options
            )
        else:
            self.__driver = webdriver.Firefox(options=self.options)

    def _open_page(self, url: HttpUrl) -> None:
        self.__driver.get(str(url))

    def _close_browser(self) -> None:
        self.__driver.quit()

    def _close_tab(self) -> None:
        self.__driver.close()

    def _reload_driver(self) -> None:
        self._close_browser()
        self.__driver = webdriver.Firefox(options=self.options)


class TutuParserConnection(Generic[T]):
    def __init__(self, tutu_parser: Type[T]) -> None:
        options = Options()
        options.add_argument('--headless')

        self.parser = tutu_parser(
            options=options,
            remote_url=settings.SELENIUM_CONF.REMOTE_URL,
        )

    def __enter__(self) -> T:
        return self.parser

    def __exit__(self, *args, **kwargs) -> None:
        self.parser._close_browser()
