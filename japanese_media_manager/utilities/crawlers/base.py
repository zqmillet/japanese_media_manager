from abc import abstractmethod
from datetime import date
from typing import List, Tuple, Dict, Optional
from bs4 import BeautifulSoup
from PIL.Image import Image

from japanese_media_manager.utilities.session import Session

class Base(Session):
    def get_metadata(self, number: str) -> dict:
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
    def get_soup(html: str) -> BeautifulSoup:
        return BeautifulSoup(html, 'html.parser')

    @abstractmethod
    def get_page_soup(self, number: str) -> BeautifulSoup:
        pass  # pragma: no cover

    @abstractmethod
    def get_fanart(self, soup: BeautifulSoup) -> Optional[Image]:
        pass  # pragma: no cover

    @abstractmethod
    def get_poster(self, soup: BeautifulSoup) -> Optional[Image]:
        pass  # pragma: no cover

    @abstractmethod
    def get_keywords(self, soup: BeautifulSoup) -> List[str]:
        pass  # pragma: no cover

    @abstractmethod
    def get_title(self, soup: BeautifulSoup) -> Optional[str]:
        pass  # pragma: no cover

    @abstractmethod
    def get_release_date(self, soup: BeautifulSoup) -> Optional[date]:
        pass  # pragma: no cover

    @abstractmethod
    def get_length(self, soup: BeautifulSoup) -> Optional[Tuple[int, str]]:
        pass  # pragma: no cover

    @abstractmethod
    def get_number(self, soup: BeautifulSoup) -> Optional[str]:
        pass  # pragma: no cover

    @abstractmethod
    def get_director(self, soup: BeautifulSoup) -> Optional[str]:
        pass  # pragma: no cover

    @abstractmethod
    def get_series(self, soup: BeautifulSoup) -> Optional[str]:
        pass  # pragma: no cover

    @abstractmethod
    def get_studio(self, soup: BeautifulSoup) -> Optional[str]:
        pass  # pragma: no cover

    @abstractmethod
    def get_outline(self, soup: BeautifulSoup) -> Optional[str]:
        pass  # pragma: no cover

    @abstractmethod
    def get_stars(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        pass  # pragma: no cover
