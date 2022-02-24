from ast import parse, Constant, Return
from textwrap import dedent
from inspect import getsource
from abc import abstractmethod
from datetime import date
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
from PIL.Image import Image

from japanese_media_manager.utilities.session import Session
from .do_nothing import do_nothing

class Base(Session):
    """
    :py:class:`Base` 继承自 :py:class:`Session` 类, 是所有 Crawler 的父类, 并且是抽象类, 其所有子类, 需要实现 :py:meth:`get_page_soup`, :py:meth:`get_fanart` 等成员方法.
    :py:class:`Base` 类会自动控制这些成员方法的调用, 并获取影片的元数据, 通过 :py:meth:`get_metadata` 方法返回给调用方.

    如果你想写另一个新网站的爬虫, 请继承该类.
    """
    all_fields = ['fanart', 'poster', 'keywords', 'title', 'release_date', 'length', 'number', 'director', 'series', 'studio', 'outline', 'stars']

    @classmethod
    def get_fields(cls) -> List[str]:
        return [field for field in cls.all_fields if not do_nothing(getattr(cls, f'get_{field}'))]

    def get_metadata(self, number: str) -> dict:
        """
        根据番号 :py:obj:`number` 获取元数据.
        """
        soup = self.get_page_soup(number)

        return {
            'fanart': self.get_fanart(soup),
            'poster': self.get_poster(soup),
            'keywords': self.get_keywords(soup),
            'title': self.get_title(soup),
            'release_date': self.get_release_date(soup),
            'length': self.get_length(soup),
            'number': self.get_number(soup) or number,
            'director': self.get_director(soup),
            'series': self.get_series(soup),
            'studio': self.get_studio(soup),
            'stars': self.get_stars(soup),
            'outline': self.get_outline(soup)
        }

    @staticmethod
    def get_soup(html: str) -> BeautifulSoup:
        """
        将 HTML 格式的字符串 :py:obj:`html` 转换成 :py:class:`BeautifulSoup`. 该函数并非虚函数, 继承时可以不用重写此函数.
        """
        return BeautifulSoup(html, 'html.parser')

    @abstractmethod
    def get_page_soup(self, number: str) -> BeautifulSoup:
        """
        该函数的作用是根据番号 :py:obj:`number` 获取影片页面的地址, 并获取 :py:obj:`BeautifulSoup` 格式的页面内容.
        """

    @abstractmethod
    def get_fanart(self, soup: BeautifulSoup) -> Optional[Image]:
        """
        从影片页面 :py:obj:`soup` 中获取 Fanart 地址, 并加载到内存中并返回图片.
        """

    @abstractmethod
    def get_poster(self, soup: BeautifulSoup) -> Optional[Image]:
        """
        从影片页面 :py:obj:`soup` 中获取海报地址, 并加载到内存中并返回图片.
        """

    @abstractmethod
    def get_keywords(self, soup: BeautifulSoup) -> List[str]:
        """
        从影片页面 :py:obj:`soup` 中获影片的关键字列表.
        """

    @abstractmethod
    def get_title(self, soup: BeautifulSoup) -> Optional[str]:
        """
        从影片页面 :py:obj:`soup` 中获影片的标题.
        """

    @abstractmethod
    def get_release_date(self, soup: BeautifulSoup) -> Optional[date]:
        """
        从影片页面 :py:obj:`soup` 中获影片的发售日期.
        """

    @abstractmethod
    def get_length(self, soup: BeautifulSoup) -> Optional[int]:
        """
        从影片页面 :py:obj:`soup` 中获影片的时长, 单位(分钟).
        """

    @abstractmethod
    def get_number(self, soup: BeautifulSoup) -> Optional[str]:
        """
        从影片页面 :py:obj:`soup` 中获影片的番号.
        """

    @abstractmethod
    def get_director(self, soup: BeautifulSoup) -> Optional[str]:
        """
        从影片页面 :py:obj:`soup` 中获影片的导演.
        """

    @abstractmethod
    def get_series(self, soup: BeautifulSoup) -> Optional[str]:
        """
        从影片页面 :py:obj:`soup` 中获影片的系列名称.
        """

    @abstractmethod
    def get_studio(self, soup: BeautifulSoup) -> Optional[str]:
        """
        从影片页面 :py:obj:`soup` 中获影片的工作室名称.
        """

    @abstractmethod
    def get_outline(self, soup: BeautifulSoup) -> Optional[str]:
        """
        从影片页面 :py:obj:`soup` 中获影片的故事梗概.
        """

    @abstractmethod
    def get_stars(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """
        从影片页面 :py:obj:`soup` 中获影片的演员列表.

        列表中的元素是一个字典, 字典中有两个字段, 分别是:

        - ``name`` 演员姓名.
        - ``avatar_url`` 头像地址.
        """
