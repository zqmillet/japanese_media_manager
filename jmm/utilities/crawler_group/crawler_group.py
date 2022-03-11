from logging import Logger
from typing import List
from typing import Optional

from jmm.utilities.logger import dumb
from jmm.utilities.metadata import Video
from jmm.crawlers import Base

class CrawlerGroup:
    """
    爬虫组, 用于管理多个爬虫, 并提供统一的输入输出.
    """

    def __init__(self, crawlers: List[Base], required_fields: Optional[List[str]] = None, logger: Logger = dumb):
        """
        :param crawlers: 爬虫列表, 列表中的爬虫存在先后顺序.
        :param required_fields: 用于指定 :py:meth:`get_metadata` 方法返回元数据的必须字段. 如果不指定该参数, 则 :py:meth:`get_metadata` 方法会抓取元数据中的所有字段.
        :param logger: 日志器, 如果不指定该参数, 则不会输出日志.
        """
        self.crawlers = crawlers
        self.logger = logger

        possible_fields = set().union(*(crawler.fields for crawler in crawlers))
        required_fields = required_fields or sorted(possible_fields)
        self.impossible_fields = set(required_fields) - possible_fields
        self.required_fields = [field for field in required_fields if field not in self.impossible_fields]
        self.logger.info('crawlers grouped by %s is ready', ', '.join(map(repr, crawlers)))
        self.logger.info('%d field(s): %s can be crawled by this crawler group', len(self.required_fields), ', '.join(self.required_fields))
        if not self.impossible_fields:
            return
        self.logger.warning('%d field(s): %s cannot be crawled by this crawler group', len(self.impossible_fields), ', '.join(sorted(self.impossible_fields)))

    def get_metadata(self, number: str) -> Optional[Video]:
        """
        该函数会依次利用 :py:obj:`self.crawlers` 列表中的爬虫爬取影片元数据.
        当元数据满足 :py:obj:`self.required_fields` 则终止爬取, 并返回元数据.
        如果多个爬虫的结果当中包含相同的字段, 则以优先爬虫的结果为准. 即前面的字段会覆盖后面的字段.

        :param number: 影片番号.
        """

        metadata = Video()
        missing_fields = set(self.required_fields)

        for crawler in self.crawlers:
            if not set(crawler.fields) & missing_fields:
                self.logger.info('%s cannot provide more fields, ignore it', crawler)
                continue

            self.logger.info('crawling video %s by %s', number, crawler)
            metadata += crawler.get_metadata(number)
            missing_fields = {field for field in missing_fields if not getattr(metadata, field, None)}

            if not missing_fields:
                self.logger.info('all fields are crawled')
                break
            self.logger.info('missing %d field(s): %s', len(missing_fields), ', '.join(sorted(missing_fields)))
        else:
            self.logger.warning('%d field(s): %s are not crawled', len(missing_fields), ', '.join(sorted(missing_fields)))

        return metadata
