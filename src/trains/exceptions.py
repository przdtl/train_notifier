from common.exceptions import TrainNotifierError, PlaywrightError


class TrainError(TrainNotifierError):
    """Базовое исключение, для ошибок, свзанных с поездами"""


class SeatSelectionButtonNotFoundError(TrainError, PlaywrightError):
    """Исключение, возникающее, если кнопка 'Выбрать места' отсутствует на странице."""
