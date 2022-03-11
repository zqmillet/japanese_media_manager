from re import match
from typing import Optional

def format_number(series: str, number: str) -> str:
    return f"{series.upper()}-{number.lstrip('0').zfill(3)}"

def get_number(file_name: str) -> Optional[str]:
    """
    根据文件名抓取文件名中包含的番号. 如果无法从文件名中获取番号, 则返回 ``None``.

    :param file_name: 不包含扩展名的文件名.
    """

    patterns = [
        r'[^a-zA-Z]*(?P<series>[a-zA-Z]+)-(?P<number>\d+).*',
        r'[^a-zA-Z]*(?P<series>[a-zA-Z]+)(?P<number>\d+).*',
    ]
    for pattern in patterns:
        result = match(pattern, file_name)
        if not result:
            continue
        return format_number(**result.groupdict())
    return None
