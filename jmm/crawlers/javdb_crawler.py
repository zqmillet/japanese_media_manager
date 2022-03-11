from re import match
from datetime import datetime, date
from io import BytesIO
from typing import List, Any, Optional
from bs4 import BeautifulSoup
from PIL.Image import Image, open as open_image

from jmm.utilities.metadata import Star

from .base import Base

class TAG:
    KEYWORDS = '類別:'
    RELEASE_DATE = '日期:'
    LENGTH = '時長:'
    DIRECTOR = '導演:'
    SERIES = '系列:'
    STUDIO = '片商:'
    STARS = '演員:'

class JavdbCrawler(Base):
    """
    JavDB 爬虫.
    """

    def __init__(self, *args: Any, base_url: str = 'https://www.javdb36.com', **kwargs: Any):
        """
        :param base_url: JavDB 的网址, 并有默认值, 如果网址发生变化, 构造实例的时候可以指定 :py:obj:`base_url`.
        :param args: 透传给父类 :py:obj:`Base`.
        :param kwargs: 透传给父类 :py:obj:`Base`.
        """
        self.base_url = base_url
        super().__init__(*args, **kwargs)

    def get_page_soup(self, number: str) -> BeautifulSoup:
        response = self.get(f'{self.base_url}/search', params={'q': number, 'f': 'all'})
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

    def get_length(self, soup: BeautifulSoup) -> Optional[int]:
        for tag in soup.find_all('div', 'panel-block'):
            strong = tag.find_next('strong')
            if not strong.text == TAG.LENGTH:
                continue

            result = match(pattern=r'(?P<number>\d+).(?P<unit>\w+)', string=strong.find_next('span').text)
            if result:
                return int(result.groupdict()['number'])
        return None

    def get_number(self, soup: BeautifulSoup) -> Optional[str]:
        for tag in soup.find_all('div', 'panel-block first-block'):
            for link in tag.find_all('a', 'button'):
                return link.attrs['data-clipboard-text']
        return None

    def get_director(self, soup: BeautifulSoup) -> Optional[str]:
        for tag in soup.find_all('div', 'panel-block'):
            strong = tag.find_next('strong')
            if not strong.text == TAG.DIRECTOR:
                continue

            return tag.find_next('span').text
        return None

    def get_series(self, soup: BeautifulSoup) -> Optional[str]:
        for tag in soup.find_all('div', 'panel-block'):
            strong = tag.find_next('strong')
            if not strong.text == TAG.SERIES:
                continue

            return tag.find_next('span').text
        return None

    def get_studio(self, soup: BeautifulSoup) -> Optional[str]:
        for tag in soup.find_all('div', 'panel-block'):
            strong = tag.find_next('strong')
            if not strong.text == TAG.STUDIO:
                continue

            return tag.find_next('span').text
        return None

    def get_stars(self, soup: BeautifulSoup) -> List[Star]:
        stars = []
        for tag in soup.find_all('div', 'panel-block'):
            strong = tag.find_next('strong')
            if not strong.text == TAG.STARS:
                continue

            for link in tag.find_all('a'):
                star = self.get_star(link.attrs['href'])
                if star:
                    stars.append(star)
        return stars

    def get_star(self, href: str) -> Optional[Star]:
        name = None
        url = None

        soup = self.get_soup(self.get(f'{self.base_url}{href}').text)
        for tag in soup.find_all('span', 'actor-section-name'):
            name = tag.text
            break

        pattern = r'.+url\((?P<url>.+)\)'
        for tag in soup.find_all('div', 'column actor-avatar'):
            result = match(pattern, tag.find_next('span').attrs['style'])
            if result:
                url = result.groupdict()['url']
                break

        if not name or not url:
            return None

        return Star(
            name=name,
            avatar_url=url,
            avatar=open_image(BytesIO(self.get(url).content))
        )
