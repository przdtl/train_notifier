from sqlalchemy import Column, ForeignKey, String, Integer, Date, Enum, UniqueConstraint

from common.db import Base
from common.types import RailwayTicketServices


class Route(Base):
    '''
    Данные о маршруте следования
    '''

    __tablename__ = 'route'

    _id = Column('id', Integer, primary_key=True, nullable=False)

    _from = Column('from', String, nullable=False)
    to = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    url = Column(String, nullable=False)
    railway_ticket_service = Column(Enum(RailwayTicketServices), nullable=False)

    __table_args__ = (
        UniqueConstraint("from", "to", "date", "railway_ticket_service", name="unique_route_for_every_service"),
    )


class UserRoutes(Base):
    '''
    Информация о маршрутах для пользователя
    '''

    __tablename__ = 'user_routes'

    user_id = Column(Integer, primary_key=True, autoincrement=False)
    route_id = Column(ForeignKey('route.id', ondelete='CASCADE'), primary_key=True)
