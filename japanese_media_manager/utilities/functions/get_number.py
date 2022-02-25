from re import match
from typing import Optional

def format_number(series: str, number: str) -> str:
    return f"{series.upper()}-{number.lstrip('0').zfill(3)}"

def get_number(number: str) -> Optional[str]:
    patterns = [
        r'[^a-zA-Z]*(?P<series>[a-zA-Z]+)-(?P<number>\d+).*',
        r'[^a-zA-Z]*(?P<series>[a-zA-Z]+)(?P<number>\d+).*',
    ]
    for pattern in patterns:
        result = match(pattern, number)
        if not result:
            continue
        return format_number(**result.groupdict())
    return None
