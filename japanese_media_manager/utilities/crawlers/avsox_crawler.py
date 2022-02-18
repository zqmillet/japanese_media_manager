import re
import io
import datetime
import PIL.Image

from .base import Base

class TAG:
    NUMBER = '识别码:'
    RELEASE_DATE = '发行时间:'
    LENGTH = '长度:'
    STUDIO = '制作商:'
    KEYWORDS = '类别:'
    SERIES = '系列:'

class AvsoxMetaData(Base):
    def __init__(self, number, base_url='https://avsox.monster', proxies=None):
        self.base_url = base_url
        super().__init__(number=number, proxies=proxies)

    def load_soup(self, number):
        response = self.session.get(f'{self.base_url}/cn/search/{number.upper()}')

        soup = self.get_soup(response.text)
        for tag in soup.find_all('div', 'item'):
            for link in tag.find_all('a'):
                if number.upper() in link.text.upper():
                    response = self.session.get(f'https:{link.attrs["href"]}')
                    self.soup = self.get_soup(response.text)
                    return

    def load_fanart(self):
        for tag in self.soup.find_all('a', 'bigImage'):
            response = self.session.get(tag.attrs['href'])
            self.fanart = PIL.Image.open(io.BytesIO(response.content))
            return

    def load_keywords(self):
        for tag in self.soup.find_all('p', 'header'):
            if not tag.text == TAG.KEYWORDS:
                continue
            for item in tag.find_next('span'):
                self.keywords.append(item.text)

    def load_series(self):
        for tag in self.soup.find_all('p', 'header'):
            if tag.text == TAG.SERIES:
                self.series = tag.find_next('p').text
                return

    def load_number(self):
        for tag in self.soup.find_all('span', 'header'):
            if tag.text == TAG.NUMBER:
                _, number_tag = tag.parent.find_all('span')
                self.number = number_tag.text
                return

    def load_release_date(self):
        for tag in self.soup.find_all('span', 'header'):
            if tag.text == TAG.RELEASE_DATE:
                self.release_date = datetime.datetime.strptime(tag.next.next.strip(), '%Y-%m-%d').date()
                return

    def load_length(self):
        for tag in self.soup.find_all('span', 'header'):
            if tag.text == TAG.LENGTH:
                match = re.match(pattern=r'(?P<number>\d+)(?P<unit>\w+)', string=tag.next.next.strip())
                if match:
                    self.length = (match.groupdict()['number'], match.groupdict()['unit'])
                    return

    def load_stars(self):
        for tag in self.soup.find_all('div', attrs={'id': 'avatar-waterfall'}):
            for item in tag.find_all('a', 'avatar-box'):
                self.stars.append(
                    {
                        'avatar_url': item.find_next('img').attrs['src'],
                        'name': item.find_next('span').text
                    }
                )

    def load_studio(self):
        for tag in self.soup.find_all('p', 'header'):
            if tag.text.strip() == TAG.STUDIO:
                self.studio = tag.find_next('p').text
                return

    def load_title(self):
        for tag in self.soup.find_all('h3'):
            self.title = tag.text
            return

    def load_director(self):
        pass

    def load_outline(self):
        pass
