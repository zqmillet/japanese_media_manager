import abc
import bs4

from japanese_media_manager.utilities.session import Session

class Base(Session):
    def get_metadata(self, number):
        soup = self.get_soup(number)
        fanart = self.get_fanart(soup)

        return {
            'fanart': fanart,
            'poster': self.get_poster(fanart),
            'keywords': self.get_keywords(soup),
            'title': self.get_title(soup),
            'release_date': self.get_release_date(soup),
            'length': self.get_length(soup),
            'number': self.get_number(soup),
            'director': self.get_director(soup),
            'series': self.get_series(soup),
            'studio': self.get_studio(soup),
            'stars': self.get_stars(soup),
            'outline': self.get_outline(soup)
        }

    @abc.abstractmethod
    def get_soup(self, number):
        pass # pragma: no cover

    @abc.abstractmethod
    def get_fanart(self, soup):
        pass # pragma: no cover

    @staticmethod
    def get_poster(fanart):
        if not fanart:
            return

        width, height = fanart.size
        return fanart.crop((width - height // 1.42, 0, width, height))

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
