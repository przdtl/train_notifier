import enum
import datetime

from typing import TypedDict


class TrainStatus(str, enum.Enum):
    '''
    Статус наличия билетов на поезд
    '''

    WAITING = 'waiting'
    AVAILABLE = "available"


class Train(TypedDict):
    number: str
    trip_time: datetime.time
    departure_datetime: datetime.datetime
    arrival_datetime: datetime.datetime
    url: str | None
    status: TrainStatus
