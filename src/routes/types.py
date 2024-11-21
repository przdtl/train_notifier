import datetime

from typing import TypedDict


class Route(TypedDict):
    _from: str
    to: str
    date: datetime.date
    url: str
