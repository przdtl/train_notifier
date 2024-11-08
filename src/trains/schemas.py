import datetime

from pydantic import BaseModel, PositiveInt


class StationScheme(BaseModel):
    title: str
    nnst: PositiveInt


class RouteScheme(BaseModel):
    departure: StationScheme
    arrival: StationScheme
    date: datetime.date
