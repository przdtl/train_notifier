import datetime

from sqlalchemy import select

from common.db import async_session_maker
from common.types import RailwayTicketServices

from routes.models import Route


async def get_route_url(departure_st: str, arrival_st: str, date: datetime.date, ticket_service: RailwayTicketServices) -> str | None:
    """
    Получает URL маршрута из базы данных по данным отправления, прибытия, дате и названию сервиса

    Args:
        departure_st (str): Станция отправления
        arrival_st (str): Станция прибытия
        date (str): Дата маршрута
        ticket_service (RailwayTicketServices) Название сервиса продажи железнодорожных билетов

    Returns:
        str: URL маршрута, хранящегося в БД
        None: Если данный маршрут отсутствует в БД

    """
    async with async_session_maker() as session:
        query = (
            select(Route.url)
            .where(
                Route._from == departure_st,
                Route.to == arrival_st,
                Route.date == date,
                Route.railway_ticket_service == ticket_service,
            )
        )
        result = await session.execute(query)
        url = result.scalar_one_or_none()

        return url


async def add_route(departure_st: str, arrival_st: str, date: datetime.date, url: str, ticket_service: RailwayTicketServices) -> None:
    """
    Добавляет новую запись о маршруте в базу данных

    Args:
        departure_st (str): Станция отправления
        arrival_st (str): Станция прибытия
        date (str): Дата маршрута
        url (str): URL маршрута
        ticket_service (RailwayTicketServices) Название сервиса продажи железнодорожных билетов

    """
    async with async_session_maker() as session:
        new_route = Route(
            _from=departure_st,
            to=arrival_st,
            date=date,
            url=url,
            railway_ticket_service=ticket_service,
        )
        session.add(new_route)
        await session.commit()
