import datetime

from abc import abstractmethod, ABCMeta

from playwright.async_api import Locator

from common.config import settings
from common.types import RailwayTicketServices
from common.services.playwright import BaseRailwayTicketServiceParser

from trains.types import Train, TrainStatus
from trains.utils import parse_travel_time, combine_date_time
from trains.exceptions import SeatSelectionButtonNotFoundError


class AbstractTrainParser(BaseRailwayTicketServiceParser, metaclass=ABCMeta):
    async def parse(self, url: str) -> list[Train]:
        """
        Парсит данные о поездах по данному маршруту ``url``

        Args:
            url (str): URL страницы маршрута для парсинга

        Returns:
            list[Train]: Список объектов `Train`, содержащих информацию о поездах

        """

        trains: list[Train] = []

        await self._open_page(url)
        for self._train in await self._get_trains_elements_list():
            is_available_tickets = await self._is_available_tickets()
            trains.append(
                Train(
                    number=await self._get_train_number(),
                    trip_time=await self._get_train_trip_time(),
                    departure_datetime=await self._get_train_departute_datetime(),
                    arrival_datetime=await self._get_train_arrival_datetime(),
                    url=await self._get_train_url() if is_available_tickets else None,
                    status=(
                        TrainStatus.AVAILABLE
                        if is_available_tickets
                        else TrainStatus.WAITING
                    ),
                )
            )

        return trains

    @abstractmethod
    async def _get_trains_elements_list(self) -> list[Locator]:
        """Возвращает список элементов, представляющих поезда на странице"""

    @abstractmethod
    async def _get_train_number(self) -> str:
        """Извлекает номер текущего поезда"""

    @abstractmethod
    async def _get_train_trip_time(self) -> datetime.timedelta:
        """Извлекает время в пути текущего поезда"""

    @abstractmethod
    async def _get_train_departute_datetime(self) -> datetime.datetime:
        """Извлекает дату и время отправления текущего поезда"""

    @abstractmethod
    async def _get_train_arrival_datetime(self) -> datetime.datetime:
        """Извлекает дату и время прибытия текущего поезда"""

    @abstractmethod
    async def _is_available_tickets(self) -> bool:
        """Проверяет наличие доступных билетов для текущего поезда"""

    @abstractmethod
    async def _get_train_url(self) -> str:
        """
        Извлекает URL-адрес страницы с подробной информацией о текущем поезде

        Raises:
            SeatSelectionButtonNotFoundError: При попытке получить URL страницы поезда,
                на который отсутствуют доступные билеты

        """


class TutuTrainParser(AbstractTrainParser):
    _service_name = RailwayTicketServices.TUTURU

    async def _get_trains_elements_list(self) -> list[Locator]:
        trains_list_locator = self._page.locator(
            "xpath={}".format(
                settings.TICKET_SERVICES.TUTU_CONF.XPATH.TRAINS_LIST_PAGE.TRAINS_LIST
            )
        )

        return await trains_list_locator.all()

    async def _get_train_number(self) -> str:
        train_number_locator = self._train.locator(
            "xpath={}".format(
                settings.TICKET_SERVICES.TUTU_CONF.XPATH.TRAINS_LIST_PAGE.TRAIN_NUMBER
            )
        )

        return await train_number_locator.inner_text()

    async def _get_train_trip_time(self) -> datetime.timedelta:
        train_trip_time_locator = self._train.locator(
            "xpath={}".format(
                settings.TICKET_SERVICES.TUTU_CONF.XPATH.TRAINS_LIST_PAGE.TRAIN_TRIP_TIME
            )
        )
        trip_time = await train_trip_time_locator.inner_text()

        return parse_travel_time(trip_time)

    async def _get_train_departute_datetime(self) -> datetime.datetime:
        train_departute_time_locator = self._train.locator(
            "xpath={}".format(
                settings.TICKET_SERVICES.TUTU_CONF.XPATH.TRAINS_LIST_PAGE.DEPARTURE_TIME
            )
        )
        train_departute_date_locator = self._train.locator(
            "xpath={}".format(
                settings.TICKET_SERVICES.TUTU_CONF.XPATH.TRAINS_LIST_PAGE.DEPARTURE_DATE
            )
        )
        departute_time = await train_departute_time_locator.inner_text()
        departute_date = await train_departute_date_locator.inner_text()

        return combine_date_time(departute_date, departute_time)

    async def _get_train_arrival_datetime(self) -> datetime.datetime:
        train_arrival_time_locator = self._train.locator(
            "xpath={}".format(
                settings.TICKET_SERVICES.TUTU_CONF.XPATH.TRAINS_LIST_PAGE.ARRIVAL_TIME
            )
        )
        train_arrival_date_locator = self._train.locator(
            "xpath={}".format(
                settings.TICKET_SERVICES.TUTU_CONF.XPATH.TRAINS_LIST_PAGE.ARRIVAL_DATE
            )
        )
        arrival_time = await train_arrival_time_locator.inner_text()
        arrival_date = await train_arrival_date_locator.inner_text()

        return combine_date_time(arrival_date, arrival_time)

    async def _is_available_tickets(self) -> bool:
        train_choose_seats_button = self._train.locator(
            "xpath={}".format(
                settings.TICKET_SERVICES.TUTU_CONF.XPATH.TRAINS_LIST_PAGE.CHOOSE_SEATS_BUTTON
            )
        )
        return await train_choose_seats_button.count() == 1

    async def _get_train_url(self) -> str:
        if not await self._is_available_tickets():
            raise SeatSelectionButtonNotFoundError

        train_choose_seats_button = self._train.locator(
            "xpath={}".format(
                settings.TICKET_SERVICES.TUTU_CONF.XPATH.TRAINS_LIST_PAGE.CHOOSE_SEATS_BUTTON
            )
        )
        async with self._page.context.expect_page() as new_page_action:
            await train_choose_seats_button.click()

        train_page = await new_page_action.value
        train_page_url = train_page.url
        await train_page.close()

        return train_page_url
