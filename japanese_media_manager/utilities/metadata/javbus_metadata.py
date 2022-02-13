import datetime
import re
import io
import PIL.Image

from .base import Base

class TAG:
    NUMBER = '識別碼:'
    RELASE_DATE = '發行日期:'
    LENGTH = '長度:'
    DIRECTOR = '導演:'
    STUDIO = '製作商:'
    LABEL = '發行商:'
    SERIES = '系列:'

class JavBusMetaData(Base):
    def __init__(self, number, base_url='https://www.javbus.com', proxies=None):
        self.base_url = base_url
        super().__init__(number=number, proxies=proxies)

    def load_soup(self, number):
        response = self.session.get(f'{self.base_url}/{number.upper()}')
        self.soup = self.get_soup(response.text)

    def load_fanart(self):
        for tag in self.soup.find_all('a', 'bigImage'):
            uri = tag.attrs["href"]
            url = f'{self.base_url}{uri}' if uri.startswith('/') else uri
            response = self.session.get(url)
            self.fanart = PIL.Image.open(io.BytesIO(response.content))
            return

    def load_keywords(self):
        for tag in self.soup.find_all('meta', attrs={'name': 'keywords'}):
            if 'content' in tag.attrs:
                self.keywords = tag.attrs['content'].split(',')
                return

    def load_title(self):
        for tag in self.soup.find_all('h3'):
            self.title = tag.text
            return

    def load_release_date(self):
        for tag in self.soup.find_all('span', 'header', text=TAG.RELASE_DATE):
            *_, date = tag.parent.contents
            self.release_date = datetime.datetime.strptime(date.strip(), '%Y-%m-%d').date()

    def load_length(self):
        pattern = r'(?P<minutes>\d+)(?P<unit>.+)'
        for tag in self.soup.find_all('span', 'header', text=TAG.LENGTH):
            *_, length = tag.parent.contents
            match = re.match(pattern, length.strip())
            if match:
                self.length = (int(match.groupdict()['minutes']), match.groupdict()['unit'])

    def load_number(self):
        for tag in self.soup.find_all('span', 'header', text=TAG.NUMBER):
            for item in tag.parent.find_all():
                if 'style' in item.attrs:
                    self.number = item.text
                    return

    def load_director(self):
        for tag in self.soup.find_all('span', 'header', text=TAG.DIRECTOR):
            for link in tag.parent.find_all('a'):
                self.director = link.text
                return

    def load_series(self):
        for tag in self.soup.find_all('span', 'header', text=TAG.SERIES):
            for link in tag.parent.find_all('a'):
                self.series = link.text
                return

    def load_studio(self):
        for tag in self.soup.find_all('span', 'header', text=TAG.STUDIO):
            for link in tag.parent.find_all('a'):
                self.studio = link.text
                return

    def load_stars(self):
        for tag in self.soup.find_all('div', attrs={'id': 'avatar-waterfall'}):
            for img in tag.find_all('img'):
                self.stars.append(
                    {
                        'avatar_url': self.base_url + img.attrs['src'],
                        'name': img.attrs['title']
                    }
                )

    def load_outline(self):
        self.outline = None
