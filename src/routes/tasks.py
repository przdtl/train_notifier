import logging
import datetime

from common.broker import broker

from routes.types import Route
from routes.services.playwright import TutuRoutesParser
from routes.services.sqlalchemy import get_route_url, add_route

logger = logging.getLogger(__name__)


@broker.task
async def get_route_info_from_tuturu(departure_st: str, arrival_st: str, date: datetime.date) -> Route:
    """
    Предоставляет полную информацию о маршруте следования.
    Сначала пробует получить информацию из БД, при её отсуствии,
    обращается к сайту и получает информацию от него, после чего записывает
    актуальные данные в БД

    Args:
        departure_st (str): Название станции отправления
        arrival_st (str): Название станции прибытия
        date (datetime.date): Дата отправления

    Returns:
        Route: Объект, хранящий всю информацию о маршруте следования

    """
    saved_route_url = await get_route_url(departure_st, arrival_st, date)
    if saved_route_url is not None:
        logger.debug('The get_route_info task found data for dep_st="{}" arr_st="{}" date="{}" in the DB'.format(
            departure_st,
            arrival_st,
            date
        ))
        return Route(
            _from=departure_st,
            to=arrival_st,
            date=date,
            url=saved_route_url
        )

    parser = TutuRoutesParser()
    url = await parser.parse(departure_st, arrival_st, date)
    await add_route(departure_st, arrival_st, date, url)

    logger.debug('The get_route_info task parse and write data in DB for dep_st="{}" arr_st="{}" date="{}"'.format(
        departure_st,
        arrival_st,
        date,
    ))

    return Route(
        _from=departure_st,
        to=arrival_st,
        date=date,
        url=url
    )
