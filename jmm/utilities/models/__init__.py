"""
jMM 采用 Sqlite 本地数据库缓存影片信息, 该模块即数据库对象关系映射的相关配置.
"""

from .base import Base
from .video import Video
from .star import Star

__all__ = ['Base', 'Video', 'Star']
