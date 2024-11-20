import datetime

from abc import abstractmethod, ABCMeta

from common.services.playwright import BaseRailwayTicketServiceParser

from routes.exceptions import RouteSearchURLNotSetError


class AbstractRoutesParser(BaseRailwayTicketServiceParser, metaclass=ABCMeta):
    route_search_url: str | None = None

    async def parse(self, departure_st: str, arrival_st: str, date: datetime.date) -> str:
        """
        Парсит ссылку на страницу маршрута из точки ``departure_st`` в точку ``arrival_st`` на ``date`` число

        Args:
            departure_st (str): Название станции отправления
            arrival_st (str): Название станции прибытия
            date (datetime.date): Дата отправления

        Returns:
            HttpUrl: Ссылка на страницу данного маршрута

        Raises:
            RouteNotFoundError: Маршрут по входным данным не найден
            RouteSearchURLNotSetError: URL для поиска маршрута поезда для данного сайта не задан

        """
        if self.route_search_url is None:
            raise RouteSearchURLNotSetError

        await self._open_page(self.route_search_url)
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


class TutuTicketsParser(AbstractRoutesParser):
    route_search_url = 'https://www.tutu.ru/poezda/'

    async def _input_departure_station(self, departure_st: str) -> None:
        departure_st_input = self._page.locator('xpath={}'.format(
            '//*[@id="wrapper"]/div[3]/div/form/div/div/div[1]/div/div[1]/div[1]/input'
        ))
        await departure_st_input.fill(departure_st)

    async def _input_arrival_station(self, arrival_st: str) -> None:
        arrival_st_input = self._page.locator('xpath={}'.format(
            '//*[@id="wrapper"]/div[3]/div/form/div/div/div[3]/div/div[1]/div[1]/input'
        ))
        await arrival_st_input.fill(arrival_st)

    async def _input_departure_date(self, date: datetime.date) -> None:
        date_input = self._page.locator('xpath={}'.format(
            '//*[@id="wrapper"]/div[3]/div/form/div/div/div[4]/div/div[1]/div/input'
        ))
        await date_input.fill(date.strftime('%d.%m.%Y'))

    async def _click_to_find_route_button(self) -> None:
        find_button = self._page.locator('xpath={}'.format(
            '//*[@id="wrapper"]/div[3]/div/form/div/div/div[6]/button'
        ))
        await find_button.click()

    async def _get_route_url(self) -> str:
        import asyncio
        await asyncio.sleep(10)

        await self._page.screenshot(path='screenshot.png')

        return self._page.url

    async def parse(self, departure_st: str, arrival_st: str, date: datetime.date) -> str:
        station_callout_page = await super().parse(departure_st, arrival_st, date)

        if 'https://www.tutu.ru/poezda/rasp_d.php' in station_callout_page:
            return station_callout_page

        show_route_button = self._page.locator('xpath={}'.format(
            '//*[@id="wrapper"]/div[3]/div[4]/div/div[4]/div/div/div/div/div[1]/button'
        ))
        await show_route_button.click()

        return self._page.url
