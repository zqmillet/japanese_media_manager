import pytest

from japanese_media_manager.utilities.javbus import get_metadata
from japanese_media_manager.utilities.javbus import MetaData

# @pytest.mark.parametrize(
#     'number', [
#         'STAR-325',
#         'ABP-888',
#         'ABP-960',
#         'MMNT-010',
#         'ipx-292',
#         'CEMD-011',
#         'CJOD-278',
#         '100221_001',
#         'AVSW-061',
#     ]
# )
# def test_get_metadata(number):
#     metadata = get_metadata(number)

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
def test_parse_html(number):
    with open(f'testcases/utilities/javbus/data/{number.lower()}.html', 'r', encoding='utf8') as file:
        metadata = MetaData(file.read())

    print(metadata.title)
    print(metadata.keywords)
    print(metadata.release_date)
    print(metadata.length)
    print(metadata.stars)
    print(metadata.number)
    print(metadata.director)
    print(metadata.series)
    print(metadata.studio)
