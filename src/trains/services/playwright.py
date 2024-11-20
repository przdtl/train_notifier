from pydantic import HttpUrl

from abc import abstractmethod, ABCMeta

from common.services.playwright import BaseRailwayTicketServiceParser

from trains.types import Train


class AbstractTrainParser(BaseRailwayTicketServiceParser, metaclass=ABCMeta):
    @abstractmethod
    def parse(self, url: str | HttpUrl) -> list[Train]:
        """
        Парсит данные о поездах по данному маршруту ``url``

        Args:
            url (str | HttpUrl): url страницы маршрута

        Returns:
            list[Train]: Список поездов для данного маршрута

        """


class TutuTrainParser(AbstractTrainParser):
    pass
