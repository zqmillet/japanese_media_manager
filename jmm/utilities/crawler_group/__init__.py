"""
提供 CrawlerGroup 类管理多个 Crawler 对象.
"""

from .crawler_group import CrawlerGroup
from .router import Router
from .router import Rule

__all__ = ['CrawlerGroup', 'Router', 'Rule']
