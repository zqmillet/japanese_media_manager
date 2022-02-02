import pytest

from japanese_media_manager.utilities.javbus import get_metadata
from japanese_media_manager.utilities.javbus import parse

@pytest.mark.parametrize(
    'number', [
        'STAR-325',
        'ABP-888',
        'ABP-960',
        'MMNT-010',
        'ipx-292',
        'CEMD-011',
        'CJOD-278',
        '100221_001',
        'AVSW-061',
    ]
)
def test_get_metadata(number):
    metadata = get_metadata(number)

# def test_parse_html():
#     with open('testcases/utilities/javbus/data/star-325.html', 'r', encoding='utf8') as file:
#         metadata = parse(file.read())
