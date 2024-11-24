class TrainNotifierError(Exception):
    """Базовое исключение для всех исключений проекта"""


class PlaywrightError(TrainNotifierError):
    """Базовое исключение для всех Playwright исключений"""


class BrowserNotInitializedError(PlaywrightError):
    """Исключение для случая, когда объект браузера не инициализирован"""


class ServiceNameNotSetError(PlaywrightError):
    """Исключение для случаев, когда название сервиса продажи билетов не установлено"""


class NoSuchParserInFactoryError(PlaywrightError):
    """
    Исключение для случаев, когда совершается попытка получить парсер по имени, 
    который не был зарегистрирован в фабрике
    """
