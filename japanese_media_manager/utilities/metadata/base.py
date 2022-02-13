import abc
import bs4

from japanese_media_manager.utilities.session import Session

class Base(metaclass=abc.ABCMeta):
    def __init__(self, number, proxies=None, session_initialization=None):
        self.fanart = None
        self.poster = None
        self.title = None
        self.keywords = []
        self.release_date = None
        self.length = None
        self.number = None
        self.director = None
        self.series = None
        self.studio = None
        self.outline = None
        self.stars = []
        self.session = Session(proxies=proxies, identity=self.__class__.__name__, initialization=session_initialization)
        self.parser = 'html.parser'
        self.soup = self.get_soup('')

        self.load_soup(number)
        self.load_fanart()
        self.load_poster()
        self.load_keywords()
        self.load_title()
        self.load_release_date()
        self.load_length()
        self.load_number()
        self.load_director()
        self.load_series()
        self.load_studio()
        self.load_outline()
        self.load_stars()

    def load_poster(self):
        if not self.fanart:
            return

        width, height = self.fanart.size
        self.poster = self.fanart.crop((width - height // 1.42, 0, width, height))

    @abc.abstractmethod
    def load_fanart(self):
        pass # pragma: no cover

    @abc.abstractmethod
    def load_soup(self, number):
        pass # pragma: no cover

    @abc.abstractmethod
    def load_keywords(self):
        pass # pragma: no cover

    @abc.abstractmethod
    def load_title(self):
        pass # pragma: no cover

    @abc.abstractmethod
    def load_release_date(self):
        pass # pragma: no cover

    @abc.abstractmethod
    def load_length(self):
        pass # pragma: no cover

    @abc.abstractmethod
    def load_number(self):
        pass # pragma: no cover

    @abc.abstractmethod
    def load_director(self):
        pass # pragma: no cover

    @abc.abstractmethod
    def load_series(self):
        pass # pragma: no cover

    @abc.abstractmethod
    def load_studio(self):
        pass # pragma: no cover

    @abc.abstractmethod
    def load_outline(self):
        pass # pragma: no cover

    @abc.abstractmethod
    def load_stars(self):
        pass # pragma: no cover

    def get_soup(self, html):
        return bs4.BeautifulSoup(html, self.parser)
