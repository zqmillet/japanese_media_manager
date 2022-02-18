import datetime
import re
import time

from .base import Base

class TAG:
    RELEASE_DATE = '発売日：'
    LENGHT = '収録時間：'
    NUMBER = '品番：'
    DIRECTOR = '監督：'
    SERIES = 'AVレーベル：'
    STUDIO = 'AVメーカー：'
    STARTS = 'AV女優：'

def check_age(session, base_url):
    params = {'action': 'adult_customer_agecheck', 'agecheck': '1'}
    session.get(f'{base_url}/index.php', params=params)

class ArzonMetaData(Base):
    def __init__(self, number, base_url='https://www.arzon.jp', proxies=None, interval=1):
        self.base_url = base_url
        super().__init__(number=number, proxies=proxies, session_initialization={'call': check_age, 'args': (base_url,)}, interval=interval)

    def load_soup(self, number):
        params = {'mitemcd': number, 'd': 'all', 't': 'all', 's': 'all', 'm': 'all'}
        response = self.session.get(f'{self.base_url}/itemlist.html', params=params)
        response.encoding = 'utf8'
        soup = self.get_soup(response.text)
        self.number = number

        for tag in soup.find_all('div', 'pictlist'):
            for link in tag.find_all('a'):
                response = self.session.get(f'{self.base_url}{link.attrs["href"]}')
                response.encoding = 'utf8'
                self.soup = self.get_soup(response.text)
                return

    def load_fanart(self):
        return

    def load_keywords(self):
        return

    def load_title(self):
        for tag in self.soup.find_all('h1'):
            self.title = tag.text

    def load_release_date(self):
        for tag in self.soup.find_all('td'):
            if not tag.text == TAG.RELEASE_DATE:
                continue

            match = re.match(pattern=r'(?P<date>\d+/\d+/\d+)', string=tag.find_next('td').text.strip())
            if not match:
                continue

            self.release_date = datetime.datetime.strptime(match.groupdict()['date'], '%Y/%m/%d').date()
            return

    def load_length(self):
        for tag in self.soup.find_all('td'):
            if not tag.text == TAG.LENGHT:
                continue

            match = re.match(pattern=r'(?P<length>\d+)(?P<unit>\w+)', string=tag.find_next('td').text.strip())
            if not match:
                continue
            self.length = (match.groupdict()['length'], match.groupdict()['unit'])
            return

    def load_number(self):
        return

    def load_director(self):
        for tag in self.soup.find_all('td'):
            if not tag.text == TAG.DIRECTOR:
                continue

            self.director = tag.find_next('td').text.strip()
            return

    def load_series(self):
        for tag in self.soup.find_all('td'):
            if not tag.text == TAG.SERIES:
                continue

            self.series = tag.find_next('td').text.strip()
            return

    def load_studio(self):
        for tag in self.soup.find_all('td'):
            if not tag.text == TAG.STUDIO:
                continue

            self.studio = tag.find_next('td').text.strip()
            return

    def load_stars(self):
        for tag in self.soup.find_all('td'):
            if not tag.text == TAG.STARTS:
                continue

            for link in tag.find_next('td').find_all('a'):
                time.sleep(1)
                response = self.session.get(f'{self.base_url}{link.attrs["href"]}')
                response.encoding = 'utf8'
                soup = self.get_soup(response.text)

                for item in soup.find_all('table', 'p_list1'):
                    image = item.find_next('img')
                    self.stars.append(
                        {
                            'name': image.attrs['alt'],
                            'avatar_url': f'https:{image.attrs["src"]}'
                        }
                    )

    def load_outline(self):
        for tag in self.soup.find_all('h2'):
            self.outline = tag.next.next.strip()
            return
