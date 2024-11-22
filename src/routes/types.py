import enum
import datetime

from typing import TypedDict


class RailwayTicketServices(str, enum.Enum):
    TUTURU = 'TUTURU'


class Route(TypedDict):
    _from: str
    to: str
    date: datetime.date
    url: str
    railway_ticket_service: RailwayTicketServices
