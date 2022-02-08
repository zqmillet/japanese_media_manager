import datetime
import re
import io
import bs4
import requests
import PIL.Image

from .base import Base

class ArzonMetaData(Base):
    session = None

    def __init__(self, number, base_url='https://www.arzon.jp', proxies=None):
        self.base_url = base_url
        self.proxies = proxies or {'http': None, 'https': None}
        self.load_session()

        params = {'mitemcd': number, 'd': 'all', 't': 'all', 's': 'all', 'm': 'all'}
        response = self.session.get(f'{self.base_url}/itemlist.html', params=params, proxies=self.proxies)
        response.encoding = 'utf8'
        soup = bs4.BeautifulSoup(response.text, 'html.parser')

        for tag in soup.find_all('div', 'pictlist'):
            for link in tag.find_all('a'):
                response = self.session.get(f'{self.base_url}{link.attrs["href"]}')
                response.encoding = 'utf8'
                self.soup = bs4.BeautifulSoup(response.text, 'html.parser')

        super().__init__()

    def load_session(self):
        if not ArzonMetaData.session:
            ArzonMetaData.session = requests.session()

        params = {'action': 'adult_customer_agecheck', 'agecheck': '1'}
        self.session.get(f'{self.base_url}/index.php', proxies=self.proxies, params=params)

    def load_fanart(self):
        for tag in self.soup.find_all('table', 'item_detail'):
            image = tag.find_next('img')
            url = f'https:{image.attrs["src"]}'
            response = self.session.get(url, proxies=self.proxies)
            self.fanart = PIL.Image.open(io.BytesIO(response.content))

    def load_keywords(self):
        return

    def load_title(self):
        for tag in self.soup.find_all('h1'):
            self.title = tag.text

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
