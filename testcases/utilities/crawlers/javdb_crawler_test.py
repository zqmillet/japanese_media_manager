import pytest

from japanese_media_manager.utilities.metadata import JavdbMetaData

@pytest.mark.parametrize('number', ['star-325'])
def test_javdb_metadata(number, proxies):
    metadata = JavdbMetaData(number, proxies=proxies)
    assert metadata
