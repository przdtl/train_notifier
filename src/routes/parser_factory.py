import logging

from typing import Type

from routes.types import RailwayTicketServices
from routes.exceptions import ServiceNameNotSetError
from routes.services.playwright import AbstractRoutesParser, TutuRoutesParser

logger = logging.getLogger(__name__)


class ParserFactory:
    """
    Фабрика для управления экземплярами классов парсеров.
    """

    def __init__(self):
        self.parsers: dict[RailwayTicketServices, Type[AbstractRoutesParser]] = {}

    def register_parser(self, parser_class: Type[AbstractRoutesParser]):
        """
        Регистрирует новый парсер в фабрике.
        """
        service_name = parser_class.service_name
        if service_name is None:
            raise ServiceNameNotSetError

        self.parsers[service_name] = parser_class

        logger.debug('A new parser "{}" has been added to the ParserFactory'.format(
            parser_class.__name__
        ))

    def create_parser(self, name: RailwayTicketServices) -> AbstractRoutesParser:
        """
        Создаёт экземпляр парсера по его имени.
        """
        parser_class = self.parsers.get(name)
        if not parser_class:
            raise ValueError(f"The parser named '{name}' was not found")

        parser_instance = parser_class()

        logger.debug('ParserFactory creates an instance of the "{}" class'.format(
            parser_class.__name__
        ))

        return parser_instance


parser_factory = ParserFactory()
parser_factory.register_parser(TutuRoutesParser)
