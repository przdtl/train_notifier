from abc import abstractmethod, ABCMeta

from typing import AsyncGenerator

from playwright.async_api import Locator

from common.config import settings
from common.types import RailwayTicketServices
from common.services.playwright import BaseRailwayTicketServiceParser

from tickets.exceptions import TicketsError
from tickets.types import Ticket, CarriageType, VerticalShelfPlacement, HorisontalShelfPlacement


class AbstractTicketsParser(BaseRailwayTicketServiceParser, metaclass=ABCMeta):
    async def parse(self, url: str) -> list[Ticket]:
        """
        Парсит данные о билетах со страницы поезда ``url``

        Args:
            url (str): url страницы поезда

        Returns:
            list[Ticket]: Список доступных билетов на данный поезд

        Raises:
            NoAvailableTicketsError: Доступные билеты на поезд отсутствуют

        """
        tickets_list: list[Ticket] = []

        await self._open_page(url)

        await self._parsing_preparation()

        await self._reversed_seat_carriage_parsing_preparation()
        async for reversed_seat_carriage_locator in self._get_next_reversed_seat_carriage():
            tickets_list.extend(await self._parse_reversed_seat_carriage(reversed_seat_carriage_locator))

        await self._coupe_carriage_parsing_preparation()
        async for coupe_carriage_locator in self._get_next_coupe_carriage():
            tickets_list.extend(await self._parse_coupe_carriage(coupe_carriage_locator))

        await self._sleeping_car_carriage_parsing_preparation()
        async for sleeping_car_carriage_locator in self._get_next_sleeping_car_carriage():
            tickets_list.extend(await self._parse_sleeping_car_carriage(sleeping_car_carriage_locator))

        return tickets_list

    async def _parsing_preparation(self) -> None:
        """Подготовка к парсингу"""

    async def _reversed_seat_carriage_parsing_preparation(self) -> None:
        """Подготовка к парсингу плацкатных вагонов"""

    async def _coupe_carriage_parsing_preparation(self) -> None:
        """Подготовка к парсингу купейных вагонов"""

    async def _sleeping_car_carriage_parsing_preparation(self) -> None:
        """Подготовка к парсингу вагонов СВ"""

    @abstractmethod
    async def _parse_reversed_seat_carriage(self, carriage_locator: Locator) -> list[Ticket]:
        """Парсинг плацкатных вагонов"""

    @abstractmethod
    async def _parse_coupe_carriage(self, carriage_locator: Locator) -> list[Ticket]:
        """Парсинг купейных вагонов"""

    @abstractmethod
    async def _parse_sleeping_car_carriage(self, carriage_locator: Locator) -> list[Ticket]:
        """Парсинг вагонов СВ"""

    @abstractmethod
    def _get_next_reversed_seat_carriage(self) -> AsyncGenerator[Locator, None]:
        """Метод-генератор для получения следующего локатора (элемента) плацкартного вагона"""

    @abstractmethod
    def _get_next_coupe_carriage(self) -> AsyncGenerator[Locator, None]:
        """Метод-генератор для получения следующего локатора (элемента) купейного вагона"""

    @abstractmethod
    def _get_next_sleeping_car_carriage(self) -> AsyncGenerator[Locator, None]:
        """Метод-генератор для получения следующего локатора (элемента) вагона СВ"""


class TutuTicketsParser(AbstractTicketsParser):
    _service_name = RailwayTicketServices.TUTURU

    async def _parsing_preparation(self) -> None:
        carriage_categories_locator = self._page.locator(
            'xpath=//div[contains(@data-ti, "categories_list")]/div'
        )
        carriage_category_list = await carriage_categories_locator.all()
        self.__category_carriages: dict[CarriageType, list[Locator]] = {}
        for category_locator in carriage_category_list:
            category_name = await category_locator.locator('span').first.inner_text()
            cateogry_cariages_list = await category_locator.locator('xpath=div/div').all()

            self.__category_carriages.update(
                {CarriageType(category_name): cateogry_cariages_list}
            )

    async def __get_next_carriage(self, carriage_type: CarriageType) -> AsyncGenerator[Locator, None]:
        carriage_list = self.__category_carriages.get(carriage_type, [])

        for carriage in carriage_list:
            carriage_open_info_button_locator = carriage.locator('xpath={}'.format(
                settings.TICKET_SERVICES.TUTU_CONF.XPATH.TRAIN_PAGE.OPEN_CARRIAGE_INFO_BUTTON
            ))
            await carriage_open_info_button_locator.click()

            yield carriage

            carriage_close_info_button_locator = carriage.locator('xpath={}'.format(
                settings.TICKET_SERVICES.TUTU_CONF.XPATH.TRAIN_PAGE.CLOSE_CARRIAGE_INFO_BUTTON
            ))
            await carriage_close_info_button_locator.click()

    async def _get_next_reversed_seat_carriage(self) -> AsyncGenerator[Locator, None]:
        async for carriage in self.__get_next_carriage(CarriageType.REVERSED_SEAT):
            yield carriage

    async def _get_next_coupe_carriage(self) -> AsyncGenerator[Locator, None]:
        async for carriage in self.__get_next_carriage(CarriageType.COUPE):
            yield carriage

    async def _get_next_sleeping_car_carriage(self) -> AsyncGenerator[Locator, None]:
        async for carriage in self.__get_next_carriage(CarriageType.SLEEPING_CAR):
            yield carriage

    async def _parse_reversed_seat_carriage(self, carriage_locator: Locator) -> list[Ticket]:
        tickets_list: list[Ticket] = []

        carriage_number_locator = carriage_locator.locator('xpath={}'.format(
            settings.TICKET_SERVICES.TUTU_CONF.XPATH.TRAIN_PAGE.CARRIAGE_NUMBER
        ))
        carriage_number = int(await carriage_number_locator.inner_text())
        reversed_seat_locator = carriage_locator.locator('xpath={}[@data-ti-state="active"]'.format(
            settings.TICKET_SERVICES.TUTU_CONF.XPATH.TRAIN_PAGE.SEAT_ITEM
        ))
        for seat in await reversed_seat_locator.all():
            seat_number_attribute = await seat.get_attribute('data-ti-seat')
            seat_vertical_placement_attribute = await seat.get_attribute('data-ti-type')

            if seat_number_attribute is None or seat_vertical_placement_attribute is None:
                raise TicketsError

            seat_number = int(seat_number_attribute)
            seat_vertical_placement = (
                VerticalShelfPlacement.TOP
                if seat_vertical_placement_attribute.lower() == 'top'
                else VerticalShelfPlacement.BOTTOM
            )
            seat_horisontal_placement = (
                HorisontalShelfPlacement.SIDE
                if seat_number > 36
                else HorisontalShelfPlacement.COUPE
            )

            tickets_list.append(Ticket(
                number=seat_number,
                vertical_shelf_placement=seat_vertical_placement,
                horisontal_shelf_placement=seat_horisontal_placement,
                carriage_type=CarriageType.REVERSED_SEAT,
                carriage_number=carriage_number,
            ))

        return tickets_list

    async def _parse_coupe_carriage(self, carriage_locator: Locator) -> list[Ticket]:
        tickets_list: list[Ticket] = []

        carriage_number_locator = carriage_locator.locator('xpath={}'.format(
            settings.TICKET_SERVICES.TUTU_CONF.XPATH.TRAIN_PAGE.CARRIAGE_NUMBER
        ))
        carriage_number = int(await carriage_number_locator.inner_text())

        coupe_seat_locator = carriage_locator.locator('xpath={}[@data-ti-state="active"]'.format(
            settings.TICKET_SERVICES.TUTU_CONF.XPATH.TRAIN_PAGE.SEAT_ITEM
        ))
        for seat in await coupe_seat_locator.all():
            seat_number_attribute = await seat.get_attribute('data-ti-seat')
            seat_vertical_placement_attribute = await seat.get_attribute('data-ti-type')

            if seat_number_attribute is None or seat_vertical_placement_attribute is None:
                raise TicketsError

            seat_number = int(seat_number_attribute)
            seat_vertical_placement = (
                VerticalShelfPlacement.TOP
                if seat_vertical_placement_attribute.lower() == 'top'
                else VerticalShelfPlacement.BOTTOM
            )

            tickets_list.append(Ticket(
                number=seat_number,
                vertical_shelf_placement=seat_vertical_placement,
                horisontal_shelf_placement=HorisontalShelfPlacement.COUPE,
                carriage_type=CarriageType.COUPE,
                carriage_number=carriage_number,
            ))

        return tickets_list

    async def _parse_sleeping_car_carriage(self, carriage_locator: Locator) -> list[Ticket]:
        tickets_list: list[Ticket] = []

        carriage_number_locator = carriage_locator.locator('xpath={}'.format(
            settings.TICKET_SERVICES.TUTU_CONF.XPATH.TRAIN_PAGE.CARRIAGE_NUMBER
        ))
        carriage_number = int(await carriage_number_locator.inner_text())

        sleeping_car_seat_locator = carriage_locator.locator('xpath={}[@data-ti-state="active"]'.format(
            settings.TICKET_SERVICES.TUTU_CONF.XPATH.TRAIN_PAGE.SEAT_ITEM
        ))
        for seat in await sleeping_car_seat_locator.all():
            seat_number_attribute = await seat.get_attribute('data-ti-seat')
            seat_vertical_placement_attribute = await seat.get_attribute('data-ti-type')

            if seat_number_attribute is None or seat_vertical_placement_attribute is None:
                raise TicketsError

            seat_number = int(seat_number_attribute)
            seat_vertical_placement = (
                VerticalShelfPlacement.TOP
                if seat_vertical_placement_attribute.lower() == 'top'
                else VerticalShelfPlacement.BOTTOM
            )

            tickets_list.append(Ticket(
                number=seat_number,
                vertical_shelf_placement=seat_vertical_placement,
                horisontal_shelf_placement=HorisontalShelfPlacement.COUPE,
                carriage_type=CarriageType.SLEEPING_CAR,
                carriage_number=carriage_number,
            ))

        return tickets_list
