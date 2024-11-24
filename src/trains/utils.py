import re
import datetime

MONTHS = {
    "янв": "Jan", "фев": "Feb", "мар": "Mar", "апр": "Apr", "май": "May", "июн": "Jun",
    "июл": "Jul", "авг": "Aug", "сен": "Sep", "окт": "Oct", "ноя": "Nov", "дек": "Dec"
}
DAYS = {
    "пн": "Mon", "вт": "Tue", "ср": "Wed", "чт": "Thu", "пт": "Fri", "сб": "Sat", "вс": "Sun"
}


def parse_travel_time(time_str: str) -> datetime.timedelta:
    """
    Конвертирует строку вида "12 ч 23 м в пути" или "~2 д 3 ч в пути" в timedelta

    Args:
        time_str (str): Входная строка, содержащая информацию о времени в пути

    Returns:
        timedelta: Объект timedelta, представляющий общее время

    """
    pattern = re.compile(r'~?(?:(\d+)\s*д)?\s*(?:(\d+)\s*ч)?\s*(?:(\d+)\s*м)?')
    match = pattern.search(time_str)

    if not match:
        raise ValueError("The date string could not be recognized: {}".format(time_str))

    days = int(match.group(1)) if match.group(1) else 0
    hours = int(match.group(2)) if match.group(2) else 0
    minutes = int(match.group(3)) if match.group(3) else 0

    return datetime.timedelta(days=days, hours=hours, minutes=minutes)


def make_naive(dt: datetime.datetime) -> datetime.datetime:
    """
    Преобразует объект datetime с временной зоной (offset-aware) 
    в наивный объект datetime (без информации о временной зоне).
    Если переданный объект уже наивный, он возвращается без изменений

    Args:
        dt (datetime): Объект datetime для преобразования

    Returns:
        datetime: Наивный объект datetime в UTC

    """
    if dt.tzinfo is not None:
        return dt.astimezone(datetime.timezone.utc).replace(tzinfo=None)
    return dt


def parse_russian_date(date_str: str):
    """
    Преобразует строку с датой, содержащей русские названия месяцев и дней недели,
    в строку с английскими названиями

    Args:
        date_str (str): Строка с датой, содержащая русские названия месяцев и дней недели.

    Returns:
        str: Преобразованная строка с английскими названиями месяцев и дней недели.

    """
    for ru, en in MONTHS.items():
        date_str = date_str.replace(ru, en)
    for ru, en in DAYS.items():
        date_str = date_str.replace(ru, en)

    return date_str


def combine_date_time(date_str: str, time_str: str) -> datetime.datetime:
    """
    Соединяет строки даты и времени в объект datetime

    Args:
        date_str (str): Строка с датой (например, "12 дек, чт")
        time_str (str): Строка с временем (например, "09:47")

    Returns:
        datetime: Объект datetime.datetime, представляющий указанную дату и время

    """

    en_datetime_str = f"{parse_russian_date(date_str)} {time_str}"

    try:
        date = datetime.datetime.strptime(en_datetime_str, "%d %b, %a %H:%M")
    except ValueError:
        raise ValueError(
            "The date string could not be recognized: {}".format(en_datetime_str)
        )

    return make_naive(date)
