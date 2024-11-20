from common.exceptions import TrainNotifierError, PlaywrightError


class TicketsError(TrainNotifierError):
    """Базовое исключение, для ошибок, свзанных с билетами"""


class NoAvailableTicketsError(TicketsError, PlaywrightError):
    """Исключение для случаев, когда все билеты на поезд выкуплены"""
