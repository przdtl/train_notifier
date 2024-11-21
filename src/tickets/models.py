from sqlalchemy import Column, ForeignKey, String, Enum, Integer

from common.db import Base

from tickets.types import VerticalShelfPlacement, HorisontalShelfPlacement, CarriageType


class Ticket(Base):
    '''
    Данные о билете
    '''

    __tablename__ = 'ticket'

    _id = Column('id', Integer, primary_key=True, nullable=False)

    number = Column(String, nullable=False)
    vertical_shelf_placement = Column(Enum(VerticalShelfPlacement), nullable=False)
    horisontal_shelf_placement = Column(Enum(HorisontalShelfPlacement), nullable=False)
    carriage_type = Column(Enum(CarriageType), nullable=False)
    train_id = Column(ForeignKey('train.id', ondelete='CASCADE'), nullable=False)
