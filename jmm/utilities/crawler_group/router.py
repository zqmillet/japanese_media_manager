from re import match
from typing import List
from typing import Optional

from jmm.utilities.metadata import Video

from .crawler_group import CrawlerGroup

class Rule:
    """
    爬虫路由规则.
    """
    def __init__(self, pattern: str, crawler_group: CrawlerGroup):
        r"""
        :param pattern: 番号正则表达式, 比如 ``\w+-\d+``.
        :param crawler_group: 表示爬虫组.
        """
        self.pattern = pattern
        self.crawler_group = crawler_group

class Router:
    """
    爬虫路由器.
    """
    def __init__(self, rules: List[Rule]):
        """
        :param rules: 爬虫路由规则列表.
        """
        self.rules = rules

    def get_metadata(self, number: str) -> Optional[Video]:
        """
        将番号 :py:obj:`number` 依次与 :py:obj:`rules` 中的 :py:obj:`pattern` 进行对比, 如果符合 :py:obj:`pattern`,
        则委托对应的 :py:obj:`crawler_group` 爬取数据并返回, 如果所有的规则都不匹配, 则返回 ``None``.

        :param number: 视频番号.
        """
        for rule in self.rules:
            if not match(pattern=rule.pattern, string=number):
                continue
            return rule.crawler_group.get_metadata(number)
        return None
