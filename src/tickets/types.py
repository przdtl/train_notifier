import enum

from typing import TypedDict


class VerticalShelfPlacement(str, enum.Enum):
    '''
    Вертикальное расположение места (верхнее/ нижнее)
    '''

    TOP = 'top'
    BOTTOM = 'bottom'


class HorisontalShelfPlacement(str, enum.Enum):
    '''
    Горизонтальное расположение места (боковое/ в купе)
    '''

    TOP = 'side'
    BOTTOM = 'coupe'


class CarriageType(str, enum.Enum):
    '''
    Тип вагона (плацкарт/ купе)
    '''

    REVERSED_SEAT = 'reversed_seat'
    COUPE = 'coupe'


class Ticket(TypedDict):
    number: str
    vertical_shelf_placement: VerticalShelfPlacement
    horisontal_shelf_placement: HorisontalShelfPlacement
    carriage_type: CarriageType
