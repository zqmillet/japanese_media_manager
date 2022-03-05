import pytest

from japanese_media_manager.crawlers import Base
from japanese_media_manager.crawlers import AirAvCrawler
from japanese_media_manager.crawlers import ArzonCrawler
from japanese_media_manager.crawlers import AvsoxCrawler
from japanese_media_manager.crawlers import JavdbCrawler
from japanese_media_manager.crawlers import JavBusCrawler

@pytest.mark.parametrize(
    'crawler, fields', [
        (AirAvCrawler, ['fanart', 'keywords', 'title', 'release_date', 'number', 'studio', 'outline']),
        (ArzonCrawler, ['title', 'release_date', 'length', 'director', 'series', 'studio', 'outline', 'stars']),
        (AvsoxCrawler, ['fanart', 'keywords', 'title', 'release_date', 'length', 'number', 'series', 'studio', 'stars']),
        (JavdbCrawler, ['fanart', 'keywords', 'title', 'release_date', 'length', 'number', 'director', 'series', 'studio', 'stars']),
        (JavBusCrawler, ['fanart', 'keywords', 'title', 'release_date', 'length', 'number', 'director', 'series', 'studio', 'stars']),
    ]
)
def test_class_fields(crawler, fields):
    assert crawler.fields == fields

def test_suspend_exception():
    class TestCrawler(Base):
        pass

    crawler = TestCrawler()
    response = crawler.get('http://gouliguojiashengsiyi.com')
    assert response.status_code is None
