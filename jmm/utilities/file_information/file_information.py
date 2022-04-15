from __future__ import annotations

from enum import Enum
from re import match
from typing import Optional
from typing import Dict
from typing import List
from pathlib import Path

from jmm.utilities.functions import get_number

class Direction(Enum):
    FORWARD = 1
    BACKWARD = -1

class SubtitleType(Enum):
    EMBEDDING = 0
    EXTERNEL = 1
    MIXING = 2

class Subtitle:
    def __init__(self, subtitle_type: SubtitleType, file_paths: List[Path] = None):
        self.subtitle_type = subtitle_type
        self.file_path = file_paths or []

class FileInformation:
    _instances: Dict[Path, FileInformation] = {}

    def __new__(cls, file_path: Path) -> FileInformation:
        absolute_path = file_path.absolute()
        if absolute_path not in cls._instances:
            cls._instances[absolute_path] = super().__new__(cls)
        return cls._instances[absolute_path]

    def __init__(self, file_path: Path):
        self.file_path = file_path.absolute()

    @property
    def previous(self) -> Optional[FileInformation]:
        """
        向前查找该文件的邻居.
        """
        return self._get_neighbor(direction=Direction.BACKWARD)

    @property
    def next(self) -> Optional[FileInformation]:
        """
        向后查找该文件的邻居.
        """
        return self._get_neighbor(direction=Direction.FORWARD)

    @property
    def number(self) -> Optional[str]:
        """
        获取文件名中的番号.
        """
        return get_number(self.file_path.name)

    @property
    def index(self) -> Optional[int]:
        """
        查找该文件在所有邻居中的绝对位置.

        比如文件名有一组文件:

        - ``xxx-250-cd1.mp4``,
        - ``xxx-250-cd2.mp4``,
        - ``xxx-250-cd3.mp4``.

        那么:

        - ``FileInformation(xxx-250-cd1.mp4).index`` 的值为 ``0``,
        - ``FileInformation(xxx-250-cd2.mp4).index`` 的值为 ``0``,
        - ``FileInformation(xxx-250-cd3.mp4).index`` 的值为 ``0``.
        """
        _index = 0
        point = self.previous
        while point:
            _index += 1
            point = point.previous
        return _index

    def _get_neighbor(self, direction: Direction) -> Optional[FileInformation]:
        """
        获取文件的邻居.

        有的影片会被切分成多个文件, 用 ``-CD1``, ``-CD2`` 等后缀进行区分, 这些文件属于同一部影片, 彼此互为邻居.
        邻居之间存在顺序, 顺序即为路径的字符串升序排列.
        如果找不到邻居, 则返回 :py:obj:`None`.

        :param direction: 如果值为 :py:obj:`Direction.FORWARD` 则向前找最近的一个邻居, 如果值为 :py:obj:`Direction.BACKWARD` 则向后找最近的一个邻居.
        """
        result = match(pattern=r'(?P<prefix>.*[-_][cC][dD])(?P<index>\d+)(?P<suffix>.*)', string=self.file_path.name)
        if not result:
            return None

        group = result.groupdict()
        next_file_path = self.file_path.with_name(f'{group["prefix"]}{int(group["index"]) + direction.value}{group["suffix"]}')
        if not next_file_path.is_file():
            return None

        return FileInformation(next_file_path)

    @property
    def chinese_subtitle(self) -> Optional[Subtitle]:
        """
        获取文件对应的字幕.
        """
        if self.file_path.stem.lower().endswith('-c'):
            return True
        if self.file_path.stem.lower().endswith('_c'):
            return True
        return False

    def __repr__(self) -> str:
        return f'<file {str(self.file_path)}, {self.number}, {"with" if self.chinese_subtitle else "without"} subtitle>'  # pragma: no cover

    def __hash__(self) -> int:
        return id(self)
