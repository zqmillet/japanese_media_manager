# import pytest

# from japanese_media_manager.utilities.airav import MetaData

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
# def test_metadata(number):
#     with open(f'testcases/utilities/airav/data/{number.lower()}.html', 'r', encoding='utf8') as file:
#         metadata = MetaData(file.read())

#     print(metadata.title)
#     print(metadata.outline)
#     assert metadata.length is None
#     print(metadata.keywords)
#     print(metadata.stars)
