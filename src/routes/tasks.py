import asyncio
import logging
import datetime

from common.broker import broker
from common.types import RailwayTicketServices

from routes.models import Route
from routes.exceptions import RouteNotFoundError
from routes.parser_factory import parser_factory
from routes.services.sqlalchemy import get_route_info, add_route

logger = logging.getLogger(__name__)


@broker.task
async def get_route_info_for_service(
    departure_st: str,
    arrival_st: str,
    date: datetime.date,
    ticket_service: RailwayTicketServices,
) -> Route:
    """
    Предоставляет полную информацию о маршруте следования.
    Сначала пробует получить информацию из БД, при её отсуствии,
    обращается к сайту и получает информацию от него, после чего записывает
    актуальные данные в БД

    Args:
        departure_st (str): Название станции отправления
        arrival_st (str): Название станции прибытия
        date (datetime.date): Дата отправления
        ticket_service (RailwayTicketServices) Название сервиса продажи железнодорожных билетов

    Returns:
        Route: Объект, хранящий всю информацию о маршруте следования

    """
    saved_route = await get_route_info(departure_st, arrival_st, date, ticket_service)
    if saved_route is not None:
        logger.debug(
            'The get_route_info task found data for dep_st="{}" arr_st="{}" date="{}" in the DB'.format(
                departure_st, arrival_st, date
            )
        )
        return saved_route

    parser = parser_factory.create_parser(ticket_service)
    url = await parser.parse(departure_st, arrival_st, date)
    new_route = await add_route(departure_st, arrival_st, date, url, ticket_service)

    logger.debug(
        'The get_route_info task parse and write data in DB for dep_st="{}" arr_st="{}" date="{}"'.format(
            departure_st,
            arrival_st,
            date,
        )
    )

    return new_route


@broker.task
async def get_route_services_info(
    departure_st: str,
    arrival_st: str,
    date: datetime.date,
) -> dict[RailwayTicketServices, Route]:
    """
    Получает информацию о маршрутах между двумя станциями на заданную дату в поддерживаемых сервисах продажи ЖД билетов

    Args:
        departure_st (str): Название станции отправления
        arrival_st (str): Название станции прибытия
        date (datetime.date): Дата отправления

    Returns:
        list[Route]: Список, содержащий объекты маршрутов для поддерживаемых сервисов продажи билетов

    """

    routes: dict[RailwayTicketServices, Route] = {}

    async def get_route_info_iteration(service_name: RailwayTicketServices) -> None:
        task = await get_route_info_for_service.kiq(
            departure_st, arrival_st, date, service_name
        )
        try:
            res = await task.wait_result()
            route: Route = res.return_value
        except RouteNotFoundError:
            pass
        else:
            routes.update({route.railway_ticket_service: route})

    coros = [
        get_route_info_iteration(service_name)
        for service_name in parser_factory.parsers.keys()
    ]
    await asyncio.gather(*coros)

    return routes
