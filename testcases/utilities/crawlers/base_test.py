import pytest

from japanese_media_manager.utilities.crawlers import AirAvCrawler
from japanese_media_manager.utilities.crawlers import ArzonCrawler
from japanese_media_manager.utilities.crawlers import AvsoxCrawler
from japanese_media_manager.utilities.crawlers import JavdbCrawler
from japanese_media_manager.utilities.crawlers import JavBusCrawler

@pytest.mark.parametrize(
    'crawler, fields', [
        (AirAvCrawler, ['fanart', 'keywords', 'title', 'release_date', 'number', 'studio', 'outline']),
        (ArzonCrawler, ['title', 'release_date', 'length', 'director', 'series', 'studio', 'outline', 'stars']),
        (AvsoxCrawler, ['fanart', 'keywords', 'title', 'release_date', 'length', 'number', 'series', 'studio', 'stars']),
        (JavdbCrawler, ['fanart', 'keywords', 'title', 'release_date', 'length', 'number', 'director', 'series', 'studio', 'stars']),
        (JavBusCrawler, ['fanart', 'keywords', 'title', 'release_date', 'length', 'number', 'director', 'series', 'studio', 'stars']),
    ]
)
def test_get_fields(crawler, fields):
    assert crawler.get_fields() == fields
