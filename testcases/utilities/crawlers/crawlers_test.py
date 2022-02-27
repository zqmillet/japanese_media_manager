import pytest

from japanese_media_manager.utilities.crawlers import Crawlers
from japanese_media_manager.utilities.crawlers import AirAvCrawler
from japanese_media_manager.utilities.crawlers import ArzonCrawler
from japanese_media_manager.utilities.crawlers import AvsoxCrawler
from japanese_media_manager.utilities.crawlers import JavBusCrawler
from japanese_media_manager.utilities.crawlers import JavdbCrawler

@pytest.fixture(name='airav', scope='session')
def _airav(proxies):
    return AirAvCrawler(proxies=proxies)

@pytest.fixture(name='arzon', scope='session')
def _arzon(proxies):
    return ArzonCrawler(proxies=proxies, interval=1)

@pytest.fixture(name='avsox', scope='session')
def _avsox(proxies):
    return AvsoxCrawler(proxies=proxies)

@pytest.fixture(name='javbus', scope='session')
def _javbus(proxies):
    return JavBusCrawler(proxies=proxies)

@pytest.fixture(name='javdb', scope='session')
def _javdb(proxies):
    return JavdbCrawler(proxies=proxies)

class Logger(list):
    def debug(self, message):
        self.append(('debug', message))

    def info(self, message):
        self.append(('info', message))

    def warning(self, message):
        self.append(('warning', message))

    def error(self, message):
        self.append(('error', message))

    def critical(self, message):
        self.append(('critical', message))


@pytest.fixture(name='logger', scope='function')
def _logger():
    return Logger()

def test_crawlers_warning(logger, arzon, avsox, javbus):
    Crawlers([arzon], required_fields=['poster', 'stars', 'outline'], logger=logger)
    assert logger.pop() == ('warning', "cannot get fields 'poster' by the 1 crawler(s)")
    Crawlers([avsox, arzon], required_fields=['fanart', 'stars', 'outline'], logger=logger)
    assert len(logger) == 0
    Crawlers([avsox, arzon, javbus], required_fields=['fanart', 'stars', 'outline', 'poster'], logger=logger)
    assert logger.pop() == ('warning', "cannot get fields 'poster' by the 3 crawler(s)")
