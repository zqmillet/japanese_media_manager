from __future__ import annotations
from typing import Optional
from typing import List
from datetime import date
from textwrap import indent
from textwrap import dedent
from rich.console import Console
from rich.markdown import Markdown
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
        runtime: Optional[int] = None,
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
        self.runtime = runtime
        self.release_date = release_date
        self.series = series
        self.director = director
        self.studio = studio
        self.stars = stars or []
        self.fanart = fanart
        self.poster = poster or self.get_poster_from_fanart(fanart)

    def __add__(self, other: Video) -> Video:
        return Video(
            number=self.number or other.number,
            title=self.title or other.title,
            outline=self.outline or other.outline,
            keywords=self.keywords or other.keywords,
            runtime=self.runtime or other.runtime,
            release_date=self.release_date or other.release_date,
            series=self.series or other.series,
            director=self.director or other.director,
            studio=self.studio or other.studio,
            stars=self.stars or other.stars,
            fanart=self.fanart or other.fanart,
            poster=self.poster or other.poster,
        )

    @staticmethod
    def get_poster_from_fanart(fanart: Optional[JpegImageFile]) -> Optional[JpegImageFile]:
        if not fanart:
            return None
        width, height = fanart.size
        return fanart.crop((width - height // 1.42, 0, width, height))

    @staticmethod
    def image_to_ascii(image: Optional[JpegImageFile], columns: int, line_indent: int, prefix: str = '\n') -> str:
        if not image:
            return ''
        return prefix + indent(image_to_ascii(image, columns=columns), ' ' * line_indent)

    def __repr__(self) -> str:
        console = Console()
        text = dedent(
            f'''
            - **number**: {self.number}
            - **title**: {self.title or ''}
            - **fanart**:{{}}
            - **keywords**: {', '.join(self.keywords)}
            - **outline**: {self.outline or ''}
            - **release date**: {self.release_date.strftime('%Y-%m-%d') if self.release_date else ''}
            - **runtime(min)**: {self.runtime or ''}
            - **studio**: {self.studio or ''}
            - **series**: {self.series or ''}
            - **stars**:
            '''
        )
        for star in self.stars:
            text += f'  - {star.name}{{}}\n'

        with console.capture() as capture:
            console.print(Markdown(text))

        return capture.get().format(
            Video.image_to_ascii(self.fanart, max(console.width // 2, 80), line_indent=3),
            *(Video.image_to_ascii(star.avatar, max(console.width // 4, 40), line_indent=6) for star in self.stars)
        )
