import enum

from typing import TypedDict


class VerticalShelfPlacement(str, enum.Enum):
    """
    Вертикальное расположение места (верхнее/ нижнее)
    """

    TOP = "Верхнее"
    BOTTOM = "Нижнее"


class HorisontalShelfPlacement(str, enum.Enum):
    """
    Горизонтальное расположение места (боковое/ в купе)
    """

    SIDE = "Боковое"
    COUPE = "Купе"


class CarriageType(str, enum.Enum):
    """
    Тип вагона (плацкарт/ купе)
    """

    REVERSED_SEAT = "Плацкарт"
    COUPE = "Купе"
    SLEEPING_CAR = "СВ"


class Ticket(TypedDict):
    number: int
    carriage_number: int
    vertical_shelf_placement: VerticalShelfPlacement
    horisontal_shelf_placement: HorisontalShelfPlacement
    carriage_type: CarriageType
