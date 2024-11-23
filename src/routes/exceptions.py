from common.exceptions import TrainNotifierError, PlaywrightError


class RouteError(TrainNotifierError):
    """Базовое исключение, для ошибок, свзанных с маршрутами поездов"""


class RouteNotFoundError(RouteError, PlaywrightError):
    """Исключение для случаев, когда маршрут не найден"""


class RouteSearchURLNotSetError(RouteError, PlaywrightError):
    """Исключение для случаев, когда URL для поиска маршрута поезда не задан"""


class ServiceNameNotSetError(RouteError, PlaywrightError):
    """Исключение для случаев, когда название сервиса продажи билетов не установлено"""


class NoSuchParserInFactoryError(RouteError, PlaywrightError):
    """
    Исключение для случаев, когда совершается попытка получить парсер по имени, 
    который не был зарегистрирован в фабрике
    """
