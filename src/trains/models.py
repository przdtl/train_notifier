import datetime

from sqlalchemy import Column, ForeignKey, String, DateTime, Enum, Integer, UniqueConstraint, Interval

from common.db import Base

from trains.types import TrainStatus


class Train(Base):
    '''
    Данные о поезде
    '''

    __tablename__ = 'train'

    _id = Column('id', Integer, primary_key=True, nullable=False)

    number = Column(String(50), nullable=False)
    trip_time = Column(Interval, nullable=False)
    departure_datetime = Column(DateTime, nullable=False)
    arrival_datetime = Column(DateTime, nullable=False)
    url = Column(String, nullable=True)
    route_id = Column(ForeignKey('route.id', ondelete='CASCADE'), nullable=False)
    status = Column(Enum(TrainStatus), nullable=False)

    updated_at = Column(
        DateTime,
        default=lambda: datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None),
        onupdate=lambda: datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None),
        nullable=False
    )

    __table_args__ = (
        UniqueConstraint("number", "route_id", name="unique_train_for_every_route"),
    )
