from re import match
from datetime import datetime, date
from io import BytesIO
from typing import List, Any, Tuple, Dict, Optional
from bs4 import BeautifulSoup
from PIL.Image import Image, open as open_image

from .base import Base

class TAG:
    KEYWORDS = '類別:'
    RELEASE_DATE = '日期:'
    LENGTH = '時長:'

class JavdbCrawler(Base):
    """
    JavDB 爬虫.
    """

    def __init__(self, *args: Any, base_url: str = 'https://www.javdb30.com', **kwargs: Any):
        """
        :param base_url: JavDB 的网址, 并有默认值, 如果网址发生变化, 构造实例的时候可以指定 :py:obj:`base_url`.
        :param args: 透传给父类 :py:obj:`Base`.
        :param kwargs: 透传给父类 :py:obj:`Base`.
        """
        self.base_url = base_url
        super().__init__(*args, **kwargs)

    def get_page_soup(self, number: str) -> BeautifulSoup:
        response = self.get(f'{self.base_url}/search', params={'q': number})
        soup = self.get_soup(response.text)
        for tag in soup.find_all('div', 'grid-item column'):
            for item in tag.find_all('div', 'uid'):
                if not item.text.lower() == number.lower():
                    continue
                link = tag.find_next('a')
                url = f'{self.base_url}{link.attrs["href"]}'
                response = self.get(url)
                return self.get_soup(response.text)
        return self.get_soup('')

    def get_fanart(self, soup: BeautifulSoup) -> Optional[Image]:
        for tag in soup.find_all('div', 'column column-video-cover'):
            for image in tag.find_all('img'):
                response = self.get(image.attrs['src'])
                return open_image(BytesIO(response.content))
        return None

    def get_keywords(self, soup: BeautifulSoup) -> List[str]:
        keywords = []
        for tag in soup.find_all('div', 'panel-block'):
            if not tag.find_next('strong').text == TAG.KEYWORDS:
                continue
            for link in tag.find_all('a'):
                keywords.append(link.text)
        return keywords

    def get_title(self, soup: BeautifulSoup) -> Optional[str]:
        for tag in soup.find_all('h2'):
            return tag.text.strip()
        return None

    def get_release_date(self, soup: BeautifulSoup) -> Optional[date]:
        for tag in soup.find_all('div', 'panel-block'):
            strong = tag.find_next('strong')
            if not strong.text == TAG.RELEASE_DATE:
                continue

            return datetime.strptime(strong.find_next('span').text, '%Y-%m-%d').date()
        return None

    def get_length(self, soup: BeautifulSoup) -> Optional[Tuple[int, str]]:
        for tag in soup.find_all('div', 'panel-block'):
            strong = tag.find_next('strong')
            if not strong.text == TAG.LENGTH:
                continue

            result = match(pattern=r'(?P<number>\d+).(?P<unit>\w+)', string=strong.find_next('span').text)
            if not result:
                continue

            return (result.groupdict()['number'], result.groupdict()['unit'])
        return None

    def get_number(self, soup: BeautifulSoup) -> Optional[str]:
        pass

    def get_poster(self, soup: BeautifulSoup) -> Optional[Image]:
        pass

    def get_director(self, soup: BeautifulSoup) -> Optional[str]:
        pass

    def get_series(self, soup: BeautifulSoup) -> Optional[str]:
        pass

    def get_studio(self, soup: BeautifulSoup) -> Optional[str]:
        pass

    def get_stars(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        pass

    def get_outline(self, soup: BeautifulSoup) -> Optional[str]:
        pass
