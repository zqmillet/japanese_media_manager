# import datetime
# import re
# import io
import bs4
import requests
# import PIL.Image

from .base import Base

class TAG:
    KEYWORDS = '類別:'

class JavdbMetaData(Base):
    def __init__(self, number, base_url='https://www.javdb30.com', proxies=None):
        self.soup = None
        self.base_url = base_url
        self.proxies = proxies or {'http': None, 'https': None}

        response = requests.get(f'{self.base_url}/search', params={'q': number}, proxies=proxies)
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        for tag in soup.find_all('div', 'grid-item column'):
            for item in tag.find_all('div', 'uid'):
                if not item.text.lower() == number.lower():
                    continue
                link = tag.find_next('a')
                url = f'{self.base_url}{link.attrs["href"]}'
                response = requests.get(url, proxies=proxies)
                self.soup = bs4.BeautifulSoup(response.text, 'html.parser')
                super().__init__()
                return

    def load_fanart(self):
        pass

    def load_keywords(self):
        for tag in self.soup.find_all('div', 'panel-block'):
            if not tag.find_next('strong').text == TAG.KEYWORDS:
                continue
            for link in tag.find_all('a'):
                self.keywords.append(link.text)

    def load_title(self):
        pass

    def load_release_date(self):
        pass

    def load_length(self):
        pass

    def load_number(self):
        pass

    def load_director(self):
        pass

    def load_series(self):
        pass

    def load_studio(self):
        pass

    def load_stars(self):
        pass

    def load_outline(self):
        pass
