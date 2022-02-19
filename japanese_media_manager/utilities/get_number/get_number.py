from re import match
from typing import Optional

def format_number(dictionary: dict) -> str:
    return f"{dictionary['series'].upper()}-{dictionary['number']}"

def get_number(number: str) -> Optional[str]:
    patterns = [
        r'(?P<series>[a-zA-Z]+)[ \-_\.]{0,1}(?P<number>\d+)',
        r'(?P<series>\d+)[ \-_\.](?P<number>\d+)',
    ]
    for pattern in patterns:
        result = match(pattern, number)
        if not result:
            continue
        return format_number(result.groupdict())
    return None
