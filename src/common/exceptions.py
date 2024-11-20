class TrainNotifierError(Exception):
    """Базовое исключение для всех исключений проекта"""


class PlaywrightError(TrainNotifierError):
    """Базовое исключение для всех Playwright исключений"""


class BrowserNotInitializedError(PlaywrightError):
    """Исключение для случая, когда объект браузера не инициализирован"""
