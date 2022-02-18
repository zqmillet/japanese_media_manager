import datetime
import re
import io
import PIL.Image

from .base import Base

class TAG:
    KEYWORDS = '類別:'
    RELEASE_DATE = '日期:'
    LENGTH = '時長:'

class JavdbCrawler(Base):
    def __init__(self, *args, base_url='https://www.javdb30.com', **kwargs):
        self.base_url = base_url
        super().__init__(*args, **kwargs)

    def get_page_soup(self, number):
        response = self.get(f'{self.base_url}/search', params={'q': number})
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

    def get_fanart(self, soup):
        for tag in soup.find_all('div', 'column column-video-cover'):
            for image in tag.find_all('img'):
                response = self.get(image.attrs['src'])
                return PIL.Image.open(io.BytesIO(response.content))
        return None

    def get_keywords(self, soup):
        keywords = []
        for tag in soup.find_all('div', 'panel-block'):
            if not tag.find_next('strong').text == TAG.KEYWORDS:
                continue
            for link in tag.find_all('a'):
                keywords.append(link.text)
        return keywords

    def get_title(self, soup):
        for tag in soup.find_all('h2'):
            return tag.text.strip()
        return None

    def get_release_date(self, soup):
        for tag in soup.find_all('div', 'panel-block'):
            strong = tag.find_next('strong')
            if not strong.text == TAG.RELEASE_DATE:
                continue

            return datetime.datetime.strptime(strong.find_next('span').text, '%Y-%m-%d').date()
        return None

    def get_length(self, soup):
        for tag in soup.find_all('div', 'panel-block'):
            strong = tag.find_next('strong')
            if not strong.text == TAG.LENGTH:
                continue

            match = re.match(pattern=r'(?P<number>\d+).(?P<unit>\w+)', string=strong.find_next('span').text)
            if not match:
                continue

            return (match.groupdict()['number'], match.groupdict()['unit'])
        return None

    def get_number(self, soup):
        pass

    def get_poster(self, soup):
        pass

    def get_director(self, soup):
        pass

    def get_series(self, soup):
        pass

    def get_studio(self, soup):
        pass

    def get_stars(self, soup):
        pass

    def get_outline(self, soup):
        pass
