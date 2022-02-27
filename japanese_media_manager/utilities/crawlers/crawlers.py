from logging import Logger
from typing import List
from typing import Optional
from typing import Dict

from japanese_media_manager.utilities.logger import dumb

from .base import Base

class Crawlers:
    """
    爬虫组, 用于管理多个爬虫, 并提供统一的输入输出.
    """

    def __init__(self, crawlers: List[Base], required_fields: List[str], logger: Optional[Logger] = dumb):
        """
        :param crawlers: 爬虫列表, 列表中的爬虫存在先后顺序.
        :param required_fields: :py:meth:`get_metadata` 方法返回元数据的必须字段.
        :param logger: 日志器, 如果不指定该参数, 则不会输出日志.
        """
        self.crawlers = crawlers
        self.required_fields = required_fields
        self.logger = logger

        fields = set()
        for crawler in crawlers:
            fields |= set(crawler.get_fields())

        missing_fields = set(required_fields) - fields
        if missing_fields:
            logger.warning(f'cannot get fields {", ".join(map(repr, sorted(missing_fields)))} by the {len(crawlers)} crawler(s)')

    def get_metadata(self, number: str) -> Optional[Dict]:
        """
        该函数会依次利用 :py:obj:`self.crawlers` 列表中的爬虫爬取影片元数据.
        当元数据满足 :py:obj:`self.required_fields` 则终止爬取, 并返回元数据.
        如果多个爬虫的结果当中包含相同的字段, 则以优先爬虫的结果为准.

        :param number: 影片番号.
        """
