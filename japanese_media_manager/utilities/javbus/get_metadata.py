import re
import datetime
import urllib
import http
import requests
import bs4

class TAG:
    NUMBER = '識別碼:'
    RELASE_DATE = '發行日期:'
    LENGTH = '長度:'
    DIRECTOR = '導演:'
    STUDIO = '製作商:'
    LABEL = '發行商:'
    SERIES = '系列:'

def get_metadata(number, proxies=None):
    proxies = proxies or {
        'http': None,
        'https': None,
    }

    url = f'https://www.javbus.com/{urllib.parse.quote(number)}'
    response = requests.get(url, proxies=proxies, verify=False)

    if not response.status_code == http.HTTPStatus.OK:
        raise Exception('status code error')

    return MetaData(response.json())

class MetaData:
    def __init__(self, html, base_url='https://www.javbus.com'):
        self.soup = bs4.BeautifulSoup(html, 'html.parser')
        self.base_url = base_url

    @property
    def keywords(self):
        for tag in self.soup.find_all('meta', attrs={'name': 'keywords'}):
            if 'content' in tag.attrs:
                return tag.attrs['content'].split(',')
        raise Exception('cannot find keywords')

    @property
    def title(self):
        for tag in self.soup.find_all('h3'):
            return tag.text
        raise Exception('cannot find title')

    @property
    def release_date(self):
        for tag in self.soup.find_all('span', 'header', text=TAG.RELASE_DATE):
            *_, date = tag.parent.contents
            return datetime.datetime.strptime(date.strip(), '%Y-%m-%d').date()
        raise Exception('cannot find release date')

    @property
    def length(self):
        pattern = r'(?P<minutes>\d+)(?P<unit>.+)'
        for tag in self.soup.find_all('span', 'header', text=TAG.LENGTH):
            *_, length = tag.parent.contents
            match = re.match(pattern, length.strip())
            if match:
                return int(match.groupdict()['minutes']), match.groupdict()['unit']
        raise Exception('cannot find length')

    @property
    def number(self):
        for tag in self.soup.find_all('span', 'header', text=TAG.NUMBER):
            for item in tag.parent.find_all():
                if 'style' in item.attrs:
                    return item.text
        raise Exception('cannot find number')

    @property
    def director(self):
        for tag in self.soup.find_all('span', 'header', text=TAG.DIRECTOR):
            for link in tag.parent.find_all('a'):
                return link.text
        return None

    @property
    def series(self):
        for tag in self.soup.find_all('span', 'header', text=TAG.SERIES):
            for link in tag.parent.find_all('a'):
                return link.text
        return None

    @property
    def studio(self):
        for tag in self.soup.find_all('span', 'header', text=TAG.STUDIO):
            for link in tag.parent.find_all('a'):
                return link.text
        return None

    @property
    def stars(self):
        result = []
        for tag in self.soup.find_all('div', attrs={'id': 'avatar-waterfall'}):
            for img in tag.find_all('img'):
                result.append(
                    {
                        'avatar_url': self.base_url + img.attrs['src'],
                        'name': img.attrs['title']
                    }
                )
        return result

    @property
    def outline(self):
        return None
