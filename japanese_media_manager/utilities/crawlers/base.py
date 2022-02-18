import abc
import bs4

from japanese_media_manager.utilities.session import Session

class Base(Session):
    def get_metadata(self, number):
        soup = self.get_page_soup(number)

        return {
            'fanart': self.get_fanart(soup),
            'poster': self.get_poster(soup),
            'keywords': self.get_keywords(soup),
            'title': self.get_title(soup),
            'release_date': self.get_release_date(soup),
            'length': self.get_length(soup),
            'number': self.get_number(soup) or number,
            'director': self.get_director(soup),
            'series': self.get_series(soup),
            'studio': self.get_studio(soup),
            'stars': self.get_stars(soup),
            'outline': self.get_outline(soup)
        }

    @staticmethod
    def get_soup(html):
        return bs4.BeautifulSoup(html, 'html.parser')

    @abc.abstractmethod
    def get_page_soup(self, number):
        pass # pragma: no cover

    @abc.abstractmethod
    def get_fanart(self, soup):
        pass # pragma: no cover

    @abc.abstractmethod
    def get_poster(self, soup):
        pass # pragma: no cover

    @abc.abstractmethod
    def get_keywords(self, soup):
        pass # pragma: no cover

    @abc.abstractmethod
    def get_title(self, soup):
        pass # pragma: no cover

    @abc.abstractmethod
    def get_release_date(self, soup):
        pass # pragma: no cover

    @abc.abstractmethod
    def get_length(self, soup):
        pass # pragma: no cover

    @abc.abstractmethod
    def get_number(self, soup):
        pass # pragma: no cover

    @abc.abstractmethod
    def get_director(self, soup):
        pass # pragma: no cover

    @abc.abstractmethod
    def get_series(self, soup):
        pass # pragma: no cover

    @abc.abstractmethod
    def get_studio(self, soup):
        pass # pragma: no cover

    @abc.abstractmethod
    def get_outline(self, soup):
        pass # pragma: no cover

    @abc.abstractmethod
    def get_stars(self, soup):
        pass # pragma: no cover
