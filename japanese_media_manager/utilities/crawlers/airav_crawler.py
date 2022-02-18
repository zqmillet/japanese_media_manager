import datetime
import re
import io
import PIL.Image

from .base import Base

ignore_fanart_urls = ['https://wiki-img.airav.wiki/storage/settings/February2020/fbD5j1a1wC8Anwj6csCU.jpg']

class AirAvCrawler(Base):
    def __init__(self, *args, base_url='https://cn.airav.wiki', **kwargs):
        self.base_url = base_url
        super().__init__(*args, **kwargs)

    def get_page_soup(self, number):
        response = self.get(f'{self.base_url}/video/{number.upper()}', params={'lang': 'zh-TW'})
        return self.get_soup(response.text)

    def get_outline(self, soup):
        for tag in soup.find_all('h5', 'mb-4'):
            if not tag.text.strip() == '劇情':
                continue
            for item in tag.next_elements:
                if item.name == 'p':
                    return item.text.strip()
        return None

    def get_poster(self, soup):
        return None

    def get_title(self, soup):
        for tag in soup.find_all('p', 'mb-1'):
            return tag.text.strip()
        return None

    def get_keywords(self, soup):
        result = []
        for tag in soup.find_all('div', 'tagBtnMargin'):
            for link in tag.find_all('a'):
                result.append(link.text.strip())
        return result

    def get_length(self, soup):
        return None

    def get_stars(self, soup):
        stars = []
        for tag in soup.find_all('ul', 'videoAvstarList'):
            for link in tag.find_all('a'):
                stars.append(
                    {
                        'name': link.text.strip(),
                        'avatar_url': None
                    }
                )
        return stars

    def get_director(self, soup):
        return None

    def get_series(self, soup):
        return None

    def get_studio(self, soup):
        for tag in soup.find_all('ul', 'list-unstyled pl-2'):
            for item in tag.find_all('li'):
                match = re.match(r'廠商\：(?P<studio>.+)', item.text)
                if not match:
                    continue
                return match.groupdict()['studio']
        return None

    def get_release_date(self, soup):
        for tag in soup.find_all('ul', 'list-unstyled pl-2'):
            for item in tag.find_all('li'):
                match = re.match(r'發片日期\：(?P<release_date>.+)', item.text)
                if not match:
                    continue
                return datetime.datetime.strptime(match.groupdict()['release_date'], '%Y-%m-%d').date()
        return None

    def get_fanart(self, soup):
        for tag in soup.find_all('meta', attrs={'property': 'og:image'}):
            url = tag.attrs.get('content')
            if not url or url in ignore_fanart_urls:
                continue
            response = self.get(url)
            return PIL.Image.open(io.BytesIO(response.content))
        return None

    def get_number(self, soup):
        for tag in soup.find_all('h5', 'd-none d-md-block text-primary mb-3'):
            return tag.text
        return None
