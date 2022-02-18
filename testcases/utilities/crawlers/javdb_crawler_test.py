import pytest

from japanese_media_manager.utilities.crawlers import JavdbCrawler

@pytest.mark.parametrize('number', ['star-325'])
def test_javdb_metadata(number, proxies):
    crawler = JavdbCrawler(proxies=proxies)
    metadata = crawler.get_metadata(number)
    assert metadata
