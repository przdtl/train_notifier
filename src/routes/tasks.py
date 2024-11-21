import datetime

from common.broker import broker

from routes.types import Route
from routes.services.playwright import TutuTicketsParser
from routes.services.sqlalchemy import get_route_url, add_route


@broker.task
async def get_route_info(departure_st: str, arrival_st: str, date: datetime.date) -> Route:
    saved_route_url = await get_route_url(departure_st, arrival_st, date)
    if saved_route_url is not None:
        return Route(
            _from=departure_st,
            to=arrival_st,
            date=date,
            url=saved_route_url
        )

    parser = TutuTicketsParser()
    url = await parser.parse(departure_st, arrival_st, date)
    await add_route(departure_st, arrival_st, date, url)

    return Route(
        _from=departure_st,
        to=arrival_st,
        date=date,
        url=url
    )
