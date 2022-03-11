from re import match
from datetime import datetime, date
from io import BytesIO
from typing import List, Any, Optional
from bs4 import BeautifulSoup
from PIL.Image import Image, open as open_image

from jmm.utilities.metadata import Star

from .base import Base

class TAG:
    KEYWORDS = '影片類別：'
    RELEASE_DATE = '發行時間：'
    LENGTH = '影片時長：'
    DIRECTOR = '導演：'
    STUDIO = '製作商：'
    SERIES = '系列：'
    STARS = '女優：'
    NUMBER = '番號：'

class JavBooksCrawler(Base):
    """
    JavBooks 爬虫.
    """

    def __init__(self, *args: Any, base_url: str = 'https://jmvbt.com', **kwargs: Any):
        """
        :param base_url: JavBus 的网址, 并有默认值, 如果网址发生变化, 构造实例的时候可以指定 :py:obj:`base_url`.
        :param args: 透传给父类 :py:obj:`Base`.
        :param kwargs: 透传给父类 :py:obj:`Base`.
        """
        self.base_url = base_url
        super().__init__(*args, **kwargs)

    def get_page_soup(self, number: str) -> BeautifulSoup:
        response = self.post(f'{self.base_url}/serch_censored.htm', data={'skey': number})
        for tag in self.get_soup(response.text).find_all('div', 'Po_topic'):
            if number.lower() in tag.find_next('font').text.lower():
                response = self.get(tag.find_next('a').attrs['href'])
                return self.get_soup(response.text)
        return self.get_soup('')

    def get_fanart(self, soup: BeautifulSoup) -> Optional[Image]:
        for tag in soup.find_all('div', 'info_cg'):
            url = tag.find_next('img').attrs['src']
            response = self.get(url)
            return open_image(BytesIO(response.content))
        return None

    def get_keywords(self, soup: BeautifulSoup) -> List[str]:
        keywords = []
        for tag in soup.find_all('div', 'infobox'):
            if not tag.find_next('b').text.strip() == TAG.KEYWORDS:
                continue

            for link in tag.find_all('a'):
                keywords.append(link.text)
        return keywords

    def get_title(self, soup: BeautifulSoup) -> Optional[str]:
        for tag in soup.find_all('div', attrs={'id': 'title'}):
            return tag.text
        return None

    def get_number(self, soup: BeautifulSoup) -> Optional[str]:
        for tag in soup.find_all('div', 'infobox'):
            if tag.find_next('b').text.strip() == TAG.NUMBER:
                return tag.find_next('font').text
        return None

    def get_release_date(self, soup: BeautifulSoup) -> Optional[date]:
        for tag in soup.find_all('div', 'infobox'):
            if not tag.find_next('b').text.strip() == TAG.RELEASE_DATE:
                continue

            return datetime.strptime(tag.next.next.next, '%Y-%m-%d').date()
        return None

    def get_director(self, soup: BeautifulSoup) -> Optional[str]:
        for tag in soup.find_all('div', 'infobox'):
            if tag.find_next('b').text.strip() == TAG.DIRECTOR:
                return tag.find_next('a').text
        return None

    def get_series(self, soup: BeautifulSoup) -> Optional[str]:
        for tag in soup.find_all('div', 'infobox'):
            if not tag.find_next('b').text.strip() == TAG.SERIES:
                continue

            return tag.find_next('a').text
        return None

    def get_studio(self, soup: BeautifulSoup) -> Optional[str]:
        for tag in soup.find_all('div', 'infobox'):
            if not tag.find_next('b').text.strip() == TAG.STUDIO:
                continue

            return tag.find_next('a').text
        return None

    def get_stars(self, soup: BeautifulSoup) -> List[Star]:
        stars = []
        for tag in soup.find_all('div', 'infobox'):
            if not tag.find_next('b').text.strip() == TAG.STARS:
                continue

            for item in tag.find_all('div', 'av_performer_cg_box'):
                avatar_url = item.find_next('img').attrs['src']
                stars.append(
                    Star(
                        avatar_url=avatar_url,
                        name=item.find_next('a').text,
                        avatar=open_image(BytesIO(self.get(avatar_url).content))
                    )
                )
        return stars

    def get_length(self, soup: BeautifulSoup) -> Optional[int]:
        for tag in soup.find_all('div', 'infobox'):
            if not tag.find_next('b').text.strip() == TAG.LENGTH:
                continue

            result = match(r'\D*(?P<number>\d+)\D+', tag.text)
            if result:
                return int(result.groupdict()['number'])
        return None
