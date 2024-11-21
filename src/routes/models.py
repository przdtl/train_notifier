from sqlalchemy import Column, ForeignKey, String, Integer, Date

from common.db import Base


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


class UserRoutes(Base):
    '''
    Информация о маршрутах для пользователя
    '''

    __tablename__ = 'user_routes'

    user_id = Column(Integer, primary_key=True, autoincrement=False)
    route_id = Column(ForeignKey('route.id', ondelete='CASCADE'), primary_key=True)
