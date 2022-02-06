import abc

class Base(metaclass=abc.ABCMeta):
    def __init__(self):
        self.fanart = None
        self.poster = None
        self.title = None
        self.keywords = None
        self.release_date = None
        self.length = None
        self.number = None
        self.director = None
        self.series = None
        self.studio = None
        self.outline = None
        self.stars = None

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
        pass

    @abc.abstractmethod
    def load_keywords(self):
        pass

    @abc.abstractmethod
    def load_title(self):
        pass

    @abc.abstractmethod
    def load_release_date(self):
        pass

    @abc.abstractmethod
    def load_length(self):
        pass

    @abc.abstractmethod
    def load_number(self):
        pass

    @abc.abstractmethod
    def load_director(self):
        pass

    @abc.abstractmethod
    def load_series(self):
        pass

    @abc.abstractmethod
    def load_studio(self):
        pass

    @abc.abstractmethod
    def load_outline(self):
        pass

    @abc.abstractmethod
    def load_stars(self):
        pass
