from typing import TypedDict
from pydantic import PositiveInt


class Station(TypedDict):
    title: str
    nnst: PositiveInt
    city: str


class Train(TypedDict):
    user_id: PositiveInt
    train_number: str
    trip_time: str
    departure_datetime: str
    arrival_datetime: str
    departure_station: Station
    arrival_station: Station
