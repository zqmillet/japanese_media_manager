import pytest

from jmm.crawlers import Base
from jmm.crawlers import AirAvCrawler
from jmm.crawlers import ArzonCrawler
from jmm.crawlers import AvsoxCrawler
from jmm.crawlers import JavdbCrawler
from jmm.crawlers import JavBusCrawler
from jmm.crawlers import JavBooksCrawler

@pytest.mark.parametrize(
    'crawler, fields', [
        (AirAvCrawler, ['fanart', 'keywords', 'title', 'release_date', 'number', 'studio', 'outline']),
        (ArzonCrawler, ['title', 'release_date', 'length', 'director', 'series', 'studio', 'outline']),
        (AvsoxCrawler, ['fanart', 'keywords', 'title', 'release_date', 'length', 'number', 'series', 'studio', 'stars']),
        (JavdbCrawler, ['fanart', 'keywords', 'title', 'release_date', 'length', 'number', 'director', 'series', 'studio', 'stars']),
        (JavBusCrawler, ['fanart', 'keywords', 'title', 'release_date', 'length', 'number', 'director', 'series', 'studio', 'stars']),
        (JavBooksCrawler, ['fanart', 'keywords', 'title', 'release_date', 'length', 'number', 'director', 'series', 'studio', 'stars']),
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
