import datetime
import re
import io
import PIL.Image

from .base import Base

ignore_fanart_urls = ['https://wiki-img.airav.wiki/storage/settings/February2020/fbD5j1a1wC8Anwj6csCU.jpg']

class AirAvMetaData(Base):
    def __init__(self, number, base_url='https://cn.airav.wiki', proxies=None):
        self.base_url = base_url
        super().__init__(number, proxies)

    def load_soup(self, number):
        response = self.session.get(f'{self.base_url}/video/{number.upper()}', params={'lang': 'zh-TW'})
        self.soup = self.get_soup(response.text)

    def load_outline(self):
        for tag in self.soup.find_all('h5', 'mb-4'):
            if not tag.text.strip() == '劇情':
                continue
            for item in tag.next_elements:
                if item.name == 'p':
                    self.outline = item.text.strip()
                    return

    def load_title(self):
        for tag in self.soup.find_all('p', 'mb-1'):
            self.title = tag.text.strip()
            return

    def load_keywords(self):
        result = []
        for tag in self.soup.find_all('div', 'tagBtnMargin'):
            for link in tag.find_all('a'):
                result.append(link.text.strip())
        self.keywords = result

    def load_length(self):
        return

    def load_stars(self):
        self.stars = []
        for tag in self.soup.find_all('ul', 'videoAvstarList'):
            for link in tag.find_all('a'):
                self.stars.append(
                    {
                        'name': link.text.strip(),
                        'avatar_url': None
                    }
                )

    def load_director(self):
        return

    def load_series(self):
        return

    def load_studio(self):
        for tag in self.soup.find_all('ul', 'list-unstyled pl-2'):
            for item in tag.find_all('li'):
                match = re.match(r'廠商\：(?P<studio>.+)', item.text)
                if not match:
                    continue
                self.studio = match.groupdict()['studio']

    def load_release_date(self):
        for tag in self.soup.find_all('ul', 'list-unstyled pl-2'):
            for item in tag.find_all('li'):
                match = re.match(r'發片日期\：(?P<release_date>.+)', item.text)
                if not match:
                    continue
                self.release_date = datetime.datetime.strptime(match.groupdict()['release_date'], '%Y-%m-%d').date()

    def load_fanart(self):
        for tag in self.soup.find_all('meta', attrs={'property': 'og:image'}):
            url = tag.attrs.get('content')
            if not url or url in ignore_fanart_urls:
                continue
            response = self.session.get(url)
            self.fanart = PIL.Image.open(io.BytesIO(response.content))
            return

    def load_number(self):
        for tag in self.soup.find_all('h5', 'd-none d-md-block text-primary mb-3'):
            self.number = tag.text
            return
