import bs4

from .base import Base

class AvsoxMetaData(Base):
    def __init__(self, html, base_url='https://avsox.monster/', proxies=None):
        self.soup = bs4.BeautifulSoup(html, 'html.parser')
        self.base_url = base_url
        self.proxies = proxies or {
            'http': None,
            'https': None,
        }

        super().__init__()
