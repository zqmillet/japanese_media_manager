from re import match
from datetime import datetime, date
from typing import Any
from typing import Optional
from bs4 import BeautifulSoup

from .base import Base

class TAG:
    RELEASE_DATE = '発売日：'
    LENGHT = '収録時間：'
    NUMBER = '品番：'
    DIRECTOR = '監督：'
    SERIES = 'AVレーベル：'
    STUDIO = 'AVメーカー：'
    STARTS = 'AV女優：'

class ArzonCrawler(Base):
    """
    Arzon 爬虫.
    """

    def __init__(self, *args: Any, base_url: str = 'https://www.arzon.jp', **kwargs: Any):
        """
        由于 Arzon 网站存在年龄确认环节, 因此构造时需要进行年龄确认.

        :param base_url: Arzon 的网址, 并有默认值, 如果网址发生变化, 构造实例的时候可以指定 :py:obj:`base_url`.
        :param args: 透传给父类 :py:obj:`Base`.
        :param kwargs: 透传给父类 :py:obj:`Base`.
        """
        self.base_url = base_url
        super().__init__(*args, **kwargs)
        self.get(f'{self.base_url}/index.php', params={'action': 'adult_customer_agecheck', 'agecheck': '1'})

    def get_page_soup(self, number: str) -> BeautifulSoup:
        params = {'mitemcd': number, 'd': 'all', 't': 'all', 's': 'all', 'm': 'all'}
        response = self.get(f'{self.base_url}/itemlist.html', params=params)
        response.encoding = 'utf8'
        soup = self.get_soup(response.text)

        for tag in soup.find_all('div', 'pictlist'):
            for link in tag.find_all('a'):
                response = self.get(f'{self.base_url}{link.attrs["href"]}')
                response.encoding = 'utf8'
                return self.get_soup(response.text)
        return self.get_soup('')

    def get_title(self, soup: BeautifulSoup) -> Optional[str]:
        for tag in soup.find_all('h1'):
            return tag.text
        return None

    def get_release_date(self, soup: BeautifulSoup) -> Optional[date]:
        for tag in soup.find_all('td'):
            if not tag.text == TAG.RELEASE_DATE:
                continue

            result = match(pattern=r'(?P<date>\d+/\d+/\d+)', string=tag.find_next('td').text.strip())
            if result:
                return datetime.strptime(result.groupdict()['date'], '%Y/%m/%d').date()
        return None

    def get_length(self, soup: BeautifulSoup) -> Optional[int]:
        for tag in soup.find_all('td'):
            if not tag.text == TAG.LENGHT:
                continue

            result = match(pattern=r'(?P<length>\d+)(?P<unit>\w+)', string=tag.find_next('td').text.strip())
            if result:
                return int(result.groupdict()['length'])
        return None

    def get_director(self, soup: BeautifulSoup) -> Optional[str]:
        for tag in soup.find_all('td'):
            if not tag.text == TAG.DIRECTOR:
                continue

            return tag.find_next('td').text.strip()
        return None

    def get_series(self, soup: BeautifulSoup) -> Optional[str]:
        for tag in soup.find_all('td'):
            if not tag.text == TAG.SERIES:
                continue

            return tag.find_next('td').text.strip()
        return None

    def get_studio(self, soup: BeautifulSoup) -> Optional[str]:
        for tag in soup.find_all('td'):
            if not tag.text == TAG.STUDIO:
                continue

            return tag.find_next('td').text.strip()
        return None

    def get_outline(self, soup: BeautifulSoup) -> Optional[str]:
        for tag in soup.find_all('h2'):
            return tag.next.next.strip()
        return None
