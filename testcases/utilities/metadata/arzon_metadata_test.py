import pytest

from japanese_media_manager.utilities.metadata import ArzonMetaData

@pytest.mark.parametrize(
    'number', [
        'STAR-325',
    ]
)
def test_arzon_metadata(number, proxies):
    metadata = ArzonMetaData(number, proxies=proxies)

    assert metadata.fanart is not None
