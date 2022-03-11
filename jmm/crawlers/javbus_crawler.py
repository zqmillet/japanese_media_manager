from re import match
from datetime import datetime, date
from io import BytesIO
from typing import List, Any, Optional
from bs4 import BeautifulSoup
from PIL.Image import Image, open as open_image

from jmm.utilities.metadata import Star

from .base import Base

class TAG:
    NUMBER = '識別碼:'
    RELASE_DATE = '發行日期:'
    LENGTH = '長度:'
    DIRECTOR = '導演:'
    STUDIO = '製作商:'
    LABEL = '發行商:'
    SERIES = '系列:'

class JavBusCrawler(Base):
    """
    JavBus 爬虫.
    """

    def __init__(self, *args: Any, base_url: str = 'https://www.javbus.com', **kwargs: Any):
        """
        :param base_url: JavBus 的网址, 并有默认值, 如果网址发生变化, 构造实例的时候可以指定 :py:obj:`base_url`.
        :param args: 透传给父类 :py:obj:`Base`.
        :param kwargs: 透传给父类 :py:obj:`Base`.
        """
        self.base_url = base_url
        super().__init__(*args, **kwargs)

    def get_page_soup(self, number: str) -> BeautifulSoup:
        response = self.get(f'{self.base_url}/{number.upper()}')
        return self.get_soup(response.text)

    def get_fanart(self, soup: BeautifulSoup) -> Optional[Image]:
        for tag in soup.find_all('a', 'bigImage'):
            uri = tag.attrs["href"]
            url = f'{self.base_url}{uri}' if uri.startswith('/') else uri
            response = self.get(url)
            return open_image(BytesIO(response.content))
        return None

    def get_keywords(self, soup: BeautifulSoup) -> List[str]:
        for tag in soup.find_all('meta', attrs={'name': 'keywords'}):
            if tag.attrs.get('content'):
                return tag.attrs['content'].split(',')
        return []

    def get_title(self, soup: BeautifulSoup) -> Optional[str]:
        for tag in soup.find_all('h3'):
            return tag.text
        return None

    def get_release_date(self, soup: BeautifulSoup) -> Optional[date]:
        for tag in soup.find_all('span', 'header', text=TAG.RELASE_DATE):
            *_, date_string = tag.parent.contents
            return datetime.strptime(date_string.strip(), '%Y-%m-%d').date()
        return None

    def get_length(self, soup: BeautifulSoup) -> Optional[int]:
        pattern = r'(?P<minutes>\d+)(?P<unit>.+)'
        for tag in soup.find_all('span', 'header', text=TAG.LENGTH):
            *_, length = tag.parent.contents
            result = match(pattern, length.strip())
            if result:
                return int(result.groupdict()['minutes'])
        return None

    def get_number(self, soup: BeautifulSoup) -> Optional[str]:
        for tag in soup.find_all('span', 'header', text=TAG.NUMBER):
            for item in tag.parent.find_all():
                if 'style' in item.attrs:
                    return item.text
        return None

    def get_director(self, soup: BeautifulSoup) -> Optional[str]:
        for tag in soup.find_all('span', 'header', text=TAG.DIRECTOR):
            for link in tag.parent.find_all('a'):
                return link.text
        return None

    def get_series(self, soup: BeautifulSoup) -> Optional[str]:
        for tag in soup.find_all('span', 'header', text=TAG.SERIES):
            for link in tag.parent.find_all('a'):
                return link.text
        return None

    def get_studio(self, soup: BeautifulSoup) -> Optional[str]:
        for tag in soup.find_all('span', 'header', text=TAG.STUDIO):
            for link in tag.parent.find_all('a'):
                return link.text
        return None

    def get_stars(self, soup: BeautifulSoup) -> List[Star]:
        stars = []
        for tag in soup.find_all('div', attrs={'id': 'avatar-waterfall'}):
            for img in tag.find_all('img'):
                avatar_url = self.base_url + img.attrs['src']
                stars.append(
                    Star(
                        avatar_url=avatar_url,
                        name=img.attrs['title'],
                        avatar=open_image(BytesIO(self.get(avatar_url).content))
                    )
                )
        return stars
