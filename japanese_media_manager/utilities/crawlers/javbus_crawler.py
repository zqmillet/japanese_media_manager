import datetime
import re
import io
import PIL.Image


from .get_soup import get_soup
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
    def __init__(self, *args, base_url='https://www.javbus.com', **kwargs):
        self.base_url = base_url
        super().__init__(*args, **kwargs)

    def get_soup(self, number):
        response = self.get(f'{self.base_url}/{number.upper()}')
        return get_soup(response.text)

    def get_fanart(self, soup):
        for tag in soup.find_all('a', 'bigImage'):
            uri = tag.attrs["href"]
            url = f'{self.base_url}{uri}' if uri.startswith('/') else uri
            response = self.get(url)
            return PIL.Image.open(io.BytesIO(response.content))
        return None

    def get_keywords(self, soup):
        for tag in soup.find_all('meta', attrs={'name': 'keywords'}):
            if 'content' in tag.attrs:
                return tag.attrs['content'].split(',')
        return None

    def get_title(self, soup):
        for tag in soup.find_all('h3'):
            return tag.text
        return None

    def get_release_date(self, soup):
        for tag in soup.find_all('span', 'header', text=TAG.RELASE_DATE):
            *_, date = tag.parent.contents
            return datetime.datetime.strptime(date.strip(), '%Y-%m-%d').date()
        return None

    def get_length(self, soup):
        pattern = r'(?P<minutes>\d+)(?P<unit>.+)'
        for tag in soup.find_all('span', 'header', text=TAG.LENGTH):
            *_, length = tag.parent.contents
            match = re.match(pattern, length.strip())
            if match:
                return (int(match.groupdict()['minutes']), match.groupdict()['unit'])
        return None

    def get_number(self, soup):
        for tag in soup.find_all('span', 'header', text=TAG.NUMBER):
            for item in tag.parent.find_all():
                if 'style' in item.attrs:
                    return item.text
        return None

    def get_director(self, soup):
        for tag in soup.find_all('span', 'header', text=TAG.DIRECTOR):
            for link in tag.parent.find_all('a'):
                return link.text
        return None

    def get_series(self, soup):
        for tag in soup.find_all('span', 'header', text=TAG.SERIES):
            for link in tag.parent.find_all('a'):
                return link.text
        return None

    def get_studio(self, soup):
        for tag in soup.find_all('span', 'header', text=TAG.STUDIO):
            for link in tag.parent.find_all('a'):
                return link.text
        return None

    def get_stars(self, soup):
        stars = []
        for tag in soup.find_all('div', attrs={'id': 'avatar-waterfall'}):
            for img in tag.find_all('img'):
                stars.append(
                    {
                        'avatar_url': self.base_url + img.attrs['src'],
                        'name': img.attrs['title']
                    }
                )
        return stars

    def get_outline(self, soup):
        return None
