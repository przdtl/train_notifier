import enum

from sqlalchemy import Column, ForeignKey, String, Enum, Integer

from common.db import Base


class VERTICAL_SHELF_PLACEMENT(str, enum.Enum):
    '''
    Вертикальное расположение места (верхнее/ нижнее)
    '''

    TOP = 'top'
    BOTTOM = 'bottom'


class HORISONTAL_SHELF_PLACEMENT(str, enum.Enum):
    '''
    Горизонтальное расположение места (боковое/ в купе)
    '''

    TOP = 'side'
    BOTTOM = 'coupe'


class CARRIAGE_TYPE(str, enum.Enum):
    '''
    Тип вагона (плацкарт/ купе)
    '''

    REVERSED_SEAT = 'reversed_seat'
    COUPE = 'coupe'


class Ticket(Base):
    '''
    Данные о билете
    '''

    __tablename__ = 'ticket'

    _id = Column('id', Integer, primary_key=True, nullable=False)

    number = Column(String, nullable=False)
    vertical_shelf_placement = Column(Enum(VERTICAL_SHELF_PLACEMENT), nullable=False)
    horisontal_shelf_placement = Column(Enum(HORISONTAL_SHELF_PLACEMENT), nullable=False)
    carriage_type = Column(Enum(CARRIAGE_TYPE), nullable=False)
    train_id = Column(ForeignKey('train.id', ondelete='CASCADE'), nullable=False)
