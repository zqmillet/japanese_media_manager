"""
该模块提供各种网站的爬虫, 目前支持 JavBus, AirAV, JavDB 等等. 同时也提供啦爬虫的基类 :py:class:`Base`, 如果需要开发其他网站的爬虫, 可以继承该类.
"""

from .base import Base
from .javbus_crawler import JavBusCrawler
from .airav_crawler import AirAvCrawler
from .avsox_crawler import AvsoxCrawler
from .arzon_crawler import ArzonCrawler
from .javdb_crawler import JavdbCrawler
from .javbooks_crawler import JavBooksCrawler

__all__ = ['Base', 'JavBusCrawler', 'AirAvCrawler', 'AvsoxCrawler', 'ArzonCrawler', 'JavdbCrawler', 'JavBooksCrawler']
