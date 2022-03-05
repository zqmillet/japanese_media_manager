from re import match
from typing import List
from typing import Optional

from .crawler_group import CrawlerGroup

class Rule:
    def __init__(self, pattern: str, crawler_group: CrawlerGroup):
        self.pattern = pattern
        self.crawler_group = crawler_group

class Router:
    def __init__(self, rules: List[Rule]):
        self.rules = rules

    def get_metadata(self, number: str) -> Optional[dict]:
        for rule in self.rules:
            if not match(pattern=rule.pattern, string=number):
                continue
            return rule.crawler_group.get_metadata(number)
        return None
