import re

def format_number(dictionary):
    return f"{dictionary['series'].upper()}-{dictionary['number']}"

def get_number(number):
    patterns = [
        r'(?P<series>[a-zA-Z]+)[ \-_\.]{0,1}(?P<number>\d+)',
        r'(?P<series>\d+)[ \-_\.](?P<number>\d+)',
    ]
    for pattern in patterns:
        match = re.match(pattern, number)
        if not match:
            continue
        return format_number(match.groupdict())
    return None
