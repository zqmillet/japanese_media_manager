from re import match
from datetime import datetime, date
from io import BytesIO
from typing import List
from typing import Any
from typing import Optional
from bs4 import BeautifulSoup
from PIL.Image import Image, open as open_image

from .base import Base

ignore_fanart_urls = ['https://wiki-img.airav.wiki/storage/settings/February2020/fbD5j1a1wC8Anwj6csCU.jpg']

class AirAvCrawler(Base):
    """
    AirAV 爬虫.
    """

    def __init__(self, *args: Any, base_url: str = 'https://cn.airav.wiki', **kwargs: Any):
        """
        :param base_url: AirAV 的网址, 并有默认值, 如果网址发生变化, 构造实例的时候可以指定 :py:obj:`base_url`.
        :param args: 透传给父类 :py:obj:`Base`.
        :param kwargs: 透传给父类 :py:obj:`Base`.
        """
        self.base_url = base_url
        super().__init__(*args, **kwargs)

    def get_page_soup(self, number: str) -> BeautifulSoup:
        response = self.get(f'{self.base_url}/video/{number.upper()}', params={'lang': 'zh-TW'})
        return self.get_soup(response.text)

    def get_outline(self, soup: BeautifulSoup) -> Optional[str]:
        for tag in soup.find_all('h5', 'mb-4'):
            if not tag.text.strip() == '劇情':
                continue
            for item in tag.next_elements:
                if item.name == 'p':
                    return item.text.strip()
        return None

    def get_title(self, soup: BeautifulSoup) -> Optional[str]:
        for tag in soup.find_all('p', 'mb-1'):
            return tag.text.strip()
        return None

    def get_keywords(self, soup: BeautifulSoup) -> List[str]:
        result = []
        for tag in soup.find_all('div', 'tagBtnMargin'):
            for link in tag.find_all('a'):
                result.append(link.text.strip())
        return result

    def get_studio(self, soup: BeautifulSoup) -> Optional[str]:
        for tag in soup.find_all('ul', 'list-unstyled pl-2'):
            for item in tag.find_all('li'):
                result = match(r'廠商\：(?P<studio>.+)', item.text)
                if not result:
                    continue
                return result.groupdict()['studio']
        return None

    def get_release_date(self, soup: BeautifulSoup) -> Optional[date]:
        for tag in soup.find_all('ul', 'list-unstyled pl-2'):
            for item in tag.find_all('li'):
                result = match(r'發片日期\：(?P<release_date>.+)', item.text)
                if not result:
                    continue
                return datetime.strptime(result.groupdict()['release_date'], '%Y-%m-%d').date()
        return None

    def get_fanart(self, soup: BeautifulSoup) -> Optional[Image]:
        for tag in soup.find_all('meta', attrs={'property': 'og:image'}):
            url = tag.attrs.get('content')
            if not url or url in ignore_fanart_urls:
                continue
            response = self.get(url)
            return open_image(BytesIO(response.content))
        return None

    def get_number(self, soup: BeautifulSoup) -> Optional[str]:
        for tag in soup.find_all('h5', 'd-none d-md-block text-primary mb-3'):
            return tag.text
        return None
