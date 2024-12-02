import re


def extract_number_from_string(s: str) -> int:
    """Извлекает первое встретившееся число из строки"""
    match = re.search(r"\d+", s)
    if match:
        return int(match.group())
    raise ValueError("Число не найдено в строке")
