from datetime import date
from typing import List
from typing import Optional
from typing import Any
from bs4 import BeautifulSoup
from PIL.Image import Image
from requests.models import Response
from requests.exceptions import RequestException

from jmm.utilities.session import Session
from jmm.utilities.functions import format_string
from jmm.utilities.metadata import Video
from jmm.utilities.metadata import Star

ALL_FIELDS: List[str] = ['fanart', 'poster', 'keywords', 'title', 'release_date', 'length', 'number', 'director', 'series', 'studio', 'outline', 'stars']

class MetaClass(type):
    def __init__(cls, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        _, (base_class,), *_ = args

        if base_class is Session:
            return

        cls.fields = [field for field in ALL_FIELDS if getattr(base_class, f'get_{field}') is not getattr(cls, f'get_{field}')]

class Base(Session, metaclass=MetaClass):
    """
    :py:class:`Base` 继承自 :py:class:`Session` 类, 是所有 Crawler 的父类, 并且是抽象类, 其所有子类, 需要实现 :py:meth:`get_page_soup`, :py:meth:`get_fanart` 等成员方法.
    :py:class:`Base` 类会自动控制这些成员方法的调用, 并获取影片的元数据, 通过 :py:meth:`get_metadata` 方法返回给调用方.

    如果你想写另一个新网站的爬虫, 请继承该类.
    """

    def get_metadata(self, number: str) -> Video:
        """
        根据番号 :py:obj:`number` 获取元数据.

        :param number: 影片番号.
        """
        soup = self.get_page_soup(number)

        return Video(
            fanart=self.get_fanart(soup),
            poster=self.get_poster(soup),
            keywords=list(map(format_string, self.get_keywords(soup))),
            title=format_string(self.get_title(soup)),
            release_date=self.get_release_date(soup),
            length=self.get_length(soup),
            number=format_string(self.get_number(soup) or number),
            director=format_string(self.get_director(soup)),
            series=format_string(self.get_series(soup)),
            studio=format_string(self.get_studio(soup)),
            stars=self.get_stars(soup),
            outline=format_string(self.get_outline(soup))
        )

    @staticmethod
    def get_soup(html: str) -> BeautifulSoup:
        """
        将 HTML 格式的字符串 :py:obj:`html` 转换成 :py:class:`BeautifulSoup`. 该函数并非虚函数, 继承时可以不用重写此函数.

        :param html: 网页源代码.
        """
        return BeautifulSoup(html, 'html.parser')

    def get_page_soup(self, number: str) -> BeautifulSoup:  # pylint: disable = unused-argument
        """
        该函数的作用是根据番号 :py:obj:`number` 获取影片页面的地址, 并获取 :py:obj:`BeautifulSoup` 格式的页面内容.

        :param number: 影片番号.
        """
        return self.get_soup('')  # pragma: no cover

    def get_fanart(self, soup: BeautifulSoup) -> Optional[Image]:  # pylint: disable = unused-argument, no-self-use
        """
        从影片页面 :py:obj:`soup` 中获取 Fanart 地址, 并加载到内存中并返回图片.

        :param soup: :py:class:`BeautifulSoup` 格式页面内容.
        """
        return None  # pragma: no cover

    def get_poster(self, soup: BeautifulSoup) -> Optional[Image]:  # pylint: disable = unused-argument, no-self-use
        """
        从影片页面 :py:obj:`soup` 中获取海报地址, 并加载到内存中并返回图片.

        :param soup: :py:class:`BeautifulSoup` 格式页面内容.
        """
        return None  # pragma: no cover

    def get_keywords(self, soup: BeautifulSoup) -> List[str]:  # pylint: disable = unused-argument, no-self-use
        """
        从影片页面 :py:obj:`soup` 中获影片的关键字列表.

        :param soup: :py:class:`BeautifulSoup` 格式页面内容.
        """
        return []  # pragma: no cover

    def get_title(self, soup: BeautifulSoup) -> Optional[str]:  # pylint: disable = unused-argument, no-self-use
        """
        从影片页面 :py:obj:`soup` 中获影片的标题.

        :param soup: :py:class:`BeautifulSoup` 格式页面内容.
        """
        return None  # pragma: no cover

    def get_release_date(self, soup: BeautifulSoup) -> Optional[date]:  # pylint: disable = unused-argument, no-self-use
        """
        从影片页面 :py:obj:`soup` 中获影片的发售日期.

        :param soup: :py:class:`BeautifulSoup` 格式页面内容.
        """
        return None  # pragma: no cover

    def get_length(self, soup: BeautifulSoup) -> Optional[int]:  # pylint: disable = unused-argument, no-self-use
        """
        从影片页面 :py:obj:`soup` 中获影片的时长, 单位(分钟).

        :param soup: :py:class:`BeautifulSoup` 格式页面内容.
        """
        return None  # pragma: no cover

    def get_number(self, soup: BeautifulSoup) -> Optional[str]:  # pylint: disable = unused-argument, no-self-use
        """
        从影片页面 :py:obj:`soup` 中获影片的番号.

        :param soup: :py:class:`BeautifulSoup` 格式页面内容.
        """
        return None  # pragma: no cover

    def get_director(self, soup: BeautifulSoup) -> Optional[str]:  # pylint: disable = unused-argument, no-self-use
        """
        从影片页面 :py:obj:`soup` 中获影片的导演.

        :param soup: :py:class:`BeautifulSoup` 格式页面内容.
        """
        return None  # pragma: no cover

    def get_series(self, soup: BeautifulSoup) -> Optional[str]:  # pylint: disable = unused-argument, no-self-use
        """
        从影片页面 :py:obj:`soup` 中获影片的系列名称.

        :param soup: :py:class:`BeautifulSoup` 格式页面内容.
        """
        return None  # pragma: no cover

    def get_studio(self, soup: BeautifulSoup) -> Optional[str]:  # pylint: disable = unused-argument, no-self-use
        """
        从影片页面 :py:obj:`soup` 中获影片的工作室名称.

        :param soup: :py:class:`BeautifulSoup` 格式页面内容.
        """
        return None  # pragma: no cover

    def get_outline(self, soup: BeautifulSoup) -> Optional[str]:  # pylint: disable = unused-argument, no-self-use
        """
        从影片页面 :py:obj:`soup` 中获影片的故事梗概.

        :param soup: :py:class:`BeautifulSoup` 格式页面内容.
        """
        return None  # pragma: no cover

    def get_stars(self, soup: BeautifulSoup) -> List[Star]:  # pylint: disable = unused-argument, no-self-use
        """
        从影片页面 :py:obj:`soup` 中获影片的演员列表.

        列表中的元素是一个字典, 字典中有两个字段, 分别是:

        - ``name`` 演员姓名.
        - ``avatar_url`` 头像地址.

        :param soup: :py:class:`BeautifulSoup` 格式页面内容.
        """
        return []  # pragma: no cover

    def __repr__(self) -> str:
        """
        重写函数, 便于调试.
        """
        return f'<crawler {self.__class__.__name__}>'

    def request(self, *args: Any, **kwargs: Any) -> Response:
        try:
            return super().request(*args, **kwargs)
        except RequestException:
            return Response()
