import pytest

from jmm.utilities.functions import format_string

@pytest.mark.parametrize(
    'string, formatted_string', [
        (None, None),
        ('ＢＤ－Ｓ１　ＮＯ．１　ＳＴＹＬＥ', 'ＢＤ－Ｓ１　ＮＯ．１　ＳＴＹＬＥ'),
        ('\x7f長身', '長身')
    ]
)
def test_format_string(string, formatted_string):
    assert format_string(string) == formatted_string
