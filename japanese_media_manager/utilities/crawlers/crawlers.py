from logging import Logger
from typing import List
from typing import Optional
from typing import Dict
from typing import Any

from japanese_media_manager.utilities.logger import dumb

from .base import Base

class Crawlers:
    """
    爬虫组, 用于管理多个爬虫, 并提供统一的输入输出.
    """

    def __init__(self, crawlers: List[Base], required_fields: List[str], logger: Logger = dumb):
        """
        :param crawlers: 爬虫列表, 列表中的爬虫存在先后顺序.
        :param required_fields: :py:meth:`get_metadata` 方法返回元数据的必须字段.
        :param logger: 日志器, 如果不指定该参数, 则不会输出日志.
        """
        self.crawlers = crawlers
        self.logger = logger

        fields = set()
        for crawler in crawlers:
            fields |= set(crawler.get_fields())

        self.impossible_fields = set(required_fields) - fields
        if self.impossible_fields:
            self.logger.warning('cannot get fields %s by the %d crawler(s)', ', '.join(map(repr, sorted(self.impossible_fields))), len(crawlers))

        self.required_fields = [field for field in required_fields if field not in self.impossible_fields]
        self.logger.info('crawlers grouped by %s is ready', ', '.join(map(repr, crawlers)))
        self.logger.info('%d field(s): %s can be crawled by this crawler group', len(self.required_fields), ', '.join(self.required_fields))

    def get_metadata(self, number: str) -> Optional[Dict]:
        """
        该函数会依次利用 :py:obj:`self.crawlers` 列表中的爬虫爬取影片元数据.
        当元数据满足 :py:obj:`self.required_fields` 则终止爬取, 并返回元数据.
        如果多个爬虫的结果当中包含相同的字段, 则以优先爬虫的结果为准.

        :param number: 影片番号.
        """

        metadata: Dict[str, Any] = {}
        for index, crawler in enumerate(self.crawlers, start=1):
            self.logger.info('crawling video %s by %s', number, crawler)
            for key, value in crawler.get_metadata(number).items():
                metadata[key] = metadata.get(key) or value

            missing_fields = {field for field in self.required_fields if not metadata.get(field)}

            if missing_fields:
                self.logger.info('missing %d field(s): %s', len(missing_fields), ', '.join(sorted(missing_fields)))
                continue

            self.logger.info('all required fields are ok')
            if self.crawlers[index:]:
                self.logger.info('there is no need to try rest of %d crawler(s)', len(self.crawlers) - index)
            break
        return metadata
