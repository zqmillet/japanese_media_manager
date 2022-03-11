"""
该模块提供 :py:class:`Session` 类, 利用 :py:class:`Session` 类, 可以将重试, 超时, 代理统统管理起来, 可以更加方便的爬取网站.
"""

from .session import Session

__all__ = ['Session']
