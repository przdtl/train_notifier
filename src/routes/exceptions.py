from common.exceptions import TrainNotifierError, PlaywrightError


class RouteError(TrainNotifierError):
    """Базовое исключение, для ошибок, свзанных с маршрутами поездов"""


class RouteNotFoundError(RouteError, PlaywrightError):
    """Исключение для случаев, когда маршрут не найден"""


class RouteSearchURLNotSetError(RouteError, PlaywrightError):
    """Исключение для случаев, когда URL для поиска маршрута поезда не задан"""
