import datetime

from typing import TypedDict
from pydantic import PositiveInt, BaseModel


class Station(TypedDict):
    title: str
    nnst: PositiveInt
    city: str


class Route(TypedDict):
    user_id: PositiveInt
    train_number: str
    trip_time: str
    departure_datetime: str
    arrival_datetime: str
    departure_station: Station
    arrival_station: Station
