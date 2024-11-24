import logging

from typing import Type, TypeVar, Generic

from common.types import RailwayTicketServices
from common.services.playwright import BaseRailwayTicketServiceParser
from common.exceptions import ServiceNameNotSetError, NoSuchParserInFactoryError

logger = logging.getLogger(__name__)

T = TypeVar("T", bound="BaseRailwayTicketServiceParser")


class ParserFactory(Generic[T]):
    """
    Фабрика для управления экземплярами классов парсеров.
    """

    def __init__(self):
        self.parsers: dict[RailwayTicketServices, Type[T]] = {}

    def register_parser(self, parser_class: Type[T]):
        """
        Регистрирует новый парсер в фабрике

        Args:
            parser_class (Type[BaseRailwayTicketServiceParser]): Класс парсера, который необходимо зарегистрировать.
                Должен быть наследником BaseRailwayTicketServiceParser и содержать атрибут `service_name`.

        Raises:
            ServiceNameNotSetError: Если атрибут `service_name` у переданного класса не установлен.

        """
        service_name = parser_class._service_name
        if service_name is None:
            raise ServiceNameNotSetError

        self.parsers[service_name] = parser_class

        logger.debug('A new parser "{}" has been added to the ParserFactory'.format(
            parser_class.__name__
        ))

    def create_parser(self, name: RailwayTicketServices) -> T:
        """
        Создаёт экземпляр парсера по его имени

        Args:
            name (RailwayTicketServices): Имя сервиса, для которого нужно создать парсер.
                Должен соответствовать значению `service_name` одного из зарегистрированных парсеров

        Returns:
            BaseRailwayTicketServiceParser: Экземпляр класса парсера, зарегистрированного под указанным именем

        Raises:
            NoSuchParserInFactoryError: Если парсер с указанным именем не был найден в фабрике

        """
        parser_class = self.parsers.get(name)
        if not parser_class:
            raise NoSuchParserInFactoryError

        parser_instance = parser_class()

        logger.debug('ParserFactory creates an instance of the "{}" class'.format(
            parser_class.__name__
        ))

        return parser_instance
