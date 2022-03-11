from __future__ import annotations
from typing import Optional
from typing import List
from datetime import date
from PIL.JpegImagePlugin import JpegImageFile

from jmm.utilities.functions import image_to_ascii

from .star import Star

class Video:
    def __init__(
        self,
        number: Optional[str] = None,
        title: Optional[str] = None,
        outline: Optional[str] = None,
        keywords: List[str] = None,
        length: Optional[int] = None,
        release_date: Optional[date] = None,
        series: Optional[str] = None,
        director: Optional[str] = None,
        studio: Optional[str] = None,
        stars: List[Star] = None,
        fanart: Optional[JpegImageFile] = None,
        poster: Optional[JpegImageFile] = None
    ):
        self.number = number
        self.title = title
        self.outline = outline
        self.keywords = keywords or []
        self.length = length
        self.release_date = release_date
        self.series = series
        self.director = director
        self.studio = studio
        self.stars = stars or []
        self.fanart = fanart
        self.poster = poster

    def __repr__(self) -> str:
        if not self.fanart:
            return f'<video {self.number} {self.title}>'
        return f'<video {self.number} {self.title}>\n{image_to_ascii(self.fanart)}'

    def __add__(self, other: Video) -> Video:
        return Video(
            number=self.number or other.number,
            title=self.title or other.title,
            outline=self.outline or other.outline,
            keywords=self.keywords or other.keywords,
            length=self.length or other.length,
            release_date=self.release_date or other.release_date,
            series=self.series or other.series,
            director=self.director or other.director,
            studio=self.studio or other.studio,
            stars=self.stars or other.stars,
            fanart=self.fanart or other.fanart,
            poster=self.poster or other.poster,
        )
