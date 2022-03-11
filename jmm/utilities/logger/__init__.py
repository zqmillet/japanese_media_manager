"""
本模块提供 :py:class:`Logger` 类用于记录日志, 同时也提供一个 :py:class:`Logger` 的实例 :py:obj:`dumb`, 即哑巴, 可以用作函数参数的默认值.
"""

from .logger import Logger
from .dumb import dumb

__all__ = ['Logger', 'dumb']
