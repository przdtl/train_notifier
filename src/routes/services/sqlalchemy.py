import datetime

from sqlalchemy import select

from common.db import async_session_maker

from routes.models import Route


async def get_route_url(departure_st: str, arrival_st: str, date: datetime.date) -> str | None:
    """
    Получает URL маршрута из базы данных по данным отправления, прибытия и дате

    Args:
        departure_st (str): Станция отправления
        arrival_st (str): Станция прибытия
        date (str): Дата маршрута

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
                Route.date == date
            )
        )
        result = await session.execute(query)
        url = result.scalar_one_or_none()

        return url


async def add_route(departure_st: str, arrival_st: str, date: datetime.date, url: str) -> None:
    """
    Добавляет новую запись о маршруте в базу данных

    Args:
        departure_st (str): Станция отправления
        arrival_st (str): Станция прибытия
        date (str): Дата маршрута
        url (str): URL маршрута

    """
    async with async_session_maker() as session:
        new_route = Route(
            _from=departure_st,
            to=arrival_st,
            date=date,
            url=url
        )
        session.add(new_route)
        await session.commit()
