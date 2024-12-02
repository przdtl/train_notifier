import enum
import datetime

from typing import TypedDict


class TrainStatus(str, enum.Enum):
    """
    Статус наличия билетов на поезд
    """

    WAITING = "В списке ожидания"
    AVAILABLE = "Доступны"


class Train(TypedDict):
    number: str
    trip_time: datetime.timedelta
    departure_datetime: datetime.datetime
    arrival_datetime: datetime.datetime
    url: str | None
    status: TrainStatus
