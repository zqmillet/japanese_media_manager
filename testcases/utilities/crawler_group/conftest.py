import pytest

from jmm.crawlers import AirAvCrawler
from jmm.crawlers import ArzonCrawler
from jmm.crawlers import AvsoxCrawler
from jmm.crawlers import JavBusCrawler
from jmm.crawlers import JavdbCrawler

class Logger(list):
    def debug(self, message, *args):
        self.append(('debug', message % args))

    def info(self, message, *args):
        self.append(('info', message % args))

    def warning(self, message, *args):
        self.append(('warning', message % args))

    def error(self, message, *args):
        self.append(('error', message % args))

    def critical(self, message, *args):
        self.append(('critical', message % args))

@pytest.fixture(name='logger', scope='function')
def _logger():
    return Logger()

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
