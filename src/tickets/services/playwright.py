from pydantic import HttpUrl

from abc import abstractmethod, ABCMeta

from common.services.playwright import BaseRailwayTicketServiceParser

from tickets.types import Ticket


class AbstractTicketsParser(BaseRailwayTicketServiceParser, metaclass=ABCMeta):
    @abstractmethod
    def parse(self, url: str | HttpUrl) -> list[Ticket]:
        """
        Парсит данные о билетах со страницы поезда ``url``

        Args:
            url (str | HttpUrl): url страницы поезда

        Returns:
            list[Ticket]: Список доступных билетов на данный поезд

        Raises:
            NoAvailableTicketsError: Доступные билеты на поезд отсутствуют

        """


class TutuTicketsParser(AbstractTicketsParser):
    pass
