import asyncio
import datetime

from abc import abstractmethod, ABCMeta

from playwright.async_api import TimeoutError

from common.config import settings
from common.services.playwright import BaseRailwayTicketServiceParser

from routes.types import RailwayTicketServices
from routes.exceptions import RouteSearchURLNotSetError, RouteNotFoundError


class AbstractRoutesParser(BaseRailwayTicketServiceParser, metaclass=ABCMeta):
    service_name: RailwayTicketServices | None = None
    service_route_search_url: str | None = None

    async def parse(self, departure_st: str, arrival_st: str, date: datetime.date) -> str:
        """
        Парсит ссылку на страницу маршрута из точки ``departure_st`` в точку ``arrival_st`` на ``date`` число

        Args:
            departure_st (str): Название станции отправления
            arrival_st (str): Название станции прибытия
            date (datetime.date): Дата отправления

        Returns:
            str: Ссылка на страницу данного маршрута

        Raises:
            RouteNotFoundError: Маршрут по входным данным не найден
            RouteSearchURLNotSetError: URL для поиска маршрута поезда для данного сайта не задан

        """
        if self.service_route_search_url is None:
            raise RouteSearchURLNotSetError

        await self._open_page(self.service_route_search_url)
        await self._input_departure_station(departure_st)
        await self._input_arrival_station(arrival_st)
        await self._input_departure_date(date)
        await self._click_to_find_route_button()

        return await self._get_route_url()

    @abstractmethod
    async def _input_departure_station(self, departure_st: str) -> None:
        """Вводит название станции отправления в соответствующее поле на веб-странице"""

    @abstractmethod
    async def _input_arrival_station(self, arrival_st: str) -> None:
        """Вводит название станции прибытия в соответствующее поле на веб-странице"""

    @abstractmethod
    async def _input_departure_date(self, date: datetime.date) -> None:
        """Вводит дату отправления в соответствующее поле на веб-странице"""

    @abstractmethod
    async def _click_to_find_route_button(self) -> None:
        """Нажимает на кнопку поиска маршрута на веб-странице"""

    @abstractmethod
    async def _get_route_url(self) -> str:
        """
        Получает URL страницы с результатами поиска маршрута

        Raises:
            RouteNotFoundError: Маршрут по входным данным не найден

        """


class TutuRoutesParser(AbstractRoutesParser):
    service_name = RailwayTicketServices.TUTURU
    route_search_url = settings.TICKET_SERVICES.TUTU_CONF.SEARCH_ROUTES_URL

    async def _input_departure_station(self, departure_st: str) -> None:
        departure_st_input = self._page.locator('xpath={}'.format(
            settings.TICKET_SERVICES.TUTU_CONF.XPATH.ROUTES_PAGE.DEPARTURE_ST_INPUT
        ))
        await departure_st_input.fill(departure_st)

    async def _input_arrival_station(self, arrival_st: str) -> None:
        arrival_st_input = self._page.locator('xpath={}'.format(
            settings.TICKET_SERVICES.TUTU_CONF.XPATH.ROUTES_PAGE.ARRIVAL_ST_INPUT
        ))
        await arrival_st_input.fill(arrival_st)

    async def _input_departure_date(self, date: datetime.date) -> None:
        date_input = self._page.locator('xpath={}'.format(
            settings.TICKET_SERVICES.TUTU_CONF.XPATH.ROUTES_PAGE.DATE_INPUT
        ))
        await date_input.fill(date.strftime('%d.%m.%Y'))

    async def _click_to_find_route_button(self) -> None:
        find_button = self._page.locator('xpath={}'.format(
            settings.TICKET_SERVICES.TUTU_CONF.XPATH.ROUTES_PAGE.SHOW_SCHEDULE_BUTTON
        ))
        await find_button.click()

    async def _get_route_url(self) -> str:
        await asyncio.sleep(1)

        station_callout_page = self._page.url
        if settings.TICKET_SERVICES.TUTU_CONF.TRAINS_LIST_PAGE_BASE_URL in station_callout_page:
            return station_callout_page

        show_route_button = self._page.locator('xpath={}'.format(
            settings.TICKET_SERVICES.TUTU_CONF.XPATH.ROUTES_PAGE.SHOW_ROUTE_BUTTON
        ))
        try:
            await show_route_button.click(timeout=40000)
        except TimeoutError:
            raise RouteNotFoundError

        return self._page.url
