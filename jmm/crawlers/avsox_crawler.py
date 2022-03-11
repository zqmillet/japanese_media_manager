from re import match
from datetime import datetime, date
from io import BytesIO
from typing import List, Any, Optional
from bs4 import BeautifulSoup
from PIL.Image import Image, open as open_image

from jmm.utilities.metadata import Star

from .base import Base

class TAG:
    NUMBER = '识别码:'
    RELEASE_DATE = '发行时间:'
    LENGTH = '长度:'
    STUDIO = '制作商:'
    KEYWORDS = '类别:'
    SERIES = '系列:'

class AvsoxCrawler(Base):
    """
    AVSOX 爬虫.
    """
    def __init__(self, *args: Any, base_url: str = 'https://avsox.monster', **kwargs: Any):
        """
        :param base_url: AVSOX 的网址, 并有默认值, 如果网址发生变化, 构造实例的时候可以指定 :py:obj:`base_url`.
        :param args: 透传给父类 :py:obj:`Base`.
        :param kwargs: 透传给父类 :py:obj:`Base`.
        """
        self.base_url = base_url
        super().__init__(*args, **kwargs)

    def get_page_soup(self, number: str) -> BeautifulSoup:
        response = self.get(f'{self.base_url}/cn/search/{number.upper()}')

        soup = self.get_soup(response.text)
        for tag in soup.find_all('div', 'item'):
            for link in tag.find_all('a'):
                if number.upper() in link.text.upper():
                    response = self.get(f'https:{link.attrs["href"]}')
                    return self.get_soup(response.text)
        return self.get_soup('')

    def get_fanart(self, soup: BeautifulSoup) -> Optional[Image]:
        for tag in soup.find_all('a', 'bigImage'):
            response = self.get(tag.attrs['href'])
            return open_image(BytesIO(response.content))
        return None

    def get_keywords(self, soup: BeautifulSoup) -> List[str]:
        keywords = []
        for tag in soup.find_all('p', 'header'):
            if not tag.text == TAG.KEYWORDS:
                continue
            for item in tag.find_next('span'):
                keywords.append(item.text)
        return keywords

    def get_series(self, soup: BeautifulSoup) -> Optional[str]:
        for tag in soup.find_all('p', 'header'):
            if tag.text == TAG.SERIES:
                return tag.find_next('p').text
        return None

    def get_number(self, soup: BeautifulSoup) -> Optional[str]:
        for tag in soup.find_all('span', 'header'):
            if tag.text == TAG.NUMBER:
                _, number_tag = tag.parent.find_all('span')
                return number_tag.text
        return None

    def get_release_date(self, soup: BeautifulSoup) -> Optional[date]:
        for tag in soup.find_all('span', 'header'):
            if tag.text == TAG.RELEASE_DATE:
                return datetime.strptime(tag.next.next.strip(), '%Y-%m-%d').date()
        return None

    def get_length(self, soup: BeautifulSoup) -> Optional[int]:
        for tag in soup.find_all('span', 'header'):
            if tag.text == TAG.LENGTH:
                result = match(pattern=r'(?P<number>\d+)(?P<unit>\w+)', string=tag.next.next.strip())
                if result:
                    return int(result.groupdict()['number'])
        return None

    def get_stars(self, soup: BeautifulSoup) -> List[Star]:
        stars = []
        for tag in soup.find_all('div', attrs={'id': 'avatar-waterfall'}):
            for item in tag.find_all('a', 'avatar-box'):
                avatar_url = item.find_next('img').attrs['src']
                response = self.get(avatar_url)
                avatar = open_image(BytesIO(response.content))
                stars.append(
                    Star(
                        avatar_url=avatar_url,
                        avatar=avatar,
                        name=item.find_next('span').text,
                    )
                )
        return stars

    def get_studio(self, soup: BeautifulSoup) -> Optional[str]:
        for tag in soup.find_all('p', 'header'):
            if tag.text.strip() == TAG.STUDIO:
                return tag.find_next('p').text
        return None

    def get_title(self, soup: BeautifulSoup) -> Optional[str]:
        for tag in soup.find_all('h3'):
            return tag.text
        return None
