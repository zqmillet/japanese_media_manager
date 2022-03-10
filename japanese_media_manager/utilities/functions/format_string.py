def is_printable(char: str) -> bool:
    """
    判断一个字符 :py:obj:`char` 在被打印时, 是否显示. 如果可以被打印, 那么返回 ``True``, 否则返回 ``False``.
    """
    if char in ['　']:
        return True
    return char.isprintable()

def format_string(string: str) -> str:
    """
    格式化网页中的字符串, 并做如下处理:

    - 如果字符串是 ``None``, 返回 ``None``.
    - 删除字符串中不可以被打印的字符.
    """
    if string is None:
        return None
    return ''.join(map(lambda char: char if is_printable(char) else '', string))
