import datetime

from typing import TypedDict

from common.types import RailwayTicketServices


class Route(TypedDict):
    _from: str
    to: str
    date: datetime.date
    url: str
    railway_ticket_service: RailwayTicketServices
