def is_printable(char: str) -> bool:
    if char in ['　']:
        return True
    return char.isprintable()

def format_string(string: str) -> str:
    if string is None:
        return None
    return ''.join(map(lambda char: char if is_printable(char) else '', string))
