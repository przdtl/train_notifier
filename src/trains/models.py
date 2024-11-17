import enum
import datetime

from sqlalchemy import Column, ForeignKey, String, DateTime, Time, Enum, Integer

from common.db import Base


class TrainStatus(str, enum.Enum):
    '''
    Статус наличия билетов на поезд
    '''

    WAITING = 'waiting'
    AVAILABLE = "available"


class Train(Base):
    '''
    Данные о поезде
    '''

    __tablename__ = 'train'

    _id = Column('id', Integer, primary_key=True, nullable=False)

    number = Column(String(50), nullable=False)
    trip_time = Column(Time, nullable=False)
    departure_datetime = Column(DateTime, nullable=False)
    arrival_datetime = Column(DateTime, nullable=False)
    url = Column(String, nullable=False)
    route_id = Column(ForeignKey('route.id', ondelete='CASCADE'), nullable=False)
    status = Column(Enum(TrainStatus), nullable=False)

    updated_at = Column(DateTime, default=datetime.datetime.now, nullable=False)
