from __future__ import annotations

from enum import Enum
from re import match
from typing import Optional
from typing import Dict
from pathlib import Path

from jmm.utilities.functions import get_number

class Direction(Enum):
    FORWARD = 1
    BACKWARD = -1

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
        return get_number(self.file_path.name)

    @property
    def index(self) -> Optional[int]:
        _index = 0
        point = self.previous
        while point:
            _index += 1
            point = point.previous
        return _index

    def _get_neighbor(self, direction: Direction) -> Optional[FileInformation]:
        result = match(pattern=r'(?P<prefix>.*[-_][cC][dD])(?P<index>\d+)(?P<suffix>.*)', string=self.file_path.name)
        if not result:
            return None

        group = result.groupdict()
        next_file_path = self.file_path.with_name(f'{group["prefix"]}{int(group["index"]) + direction.value}{group["suffix"]}')
        if not next_file_path.is_file():
            return None

        return FileInformation(next_file_path)

    @property
    def has_chinese_subtitle(self) -> bool:
        if self.file_path.stem.lower().endswith('-c'):
            return True
        if self.file_path.stem.lower().endswith('_c'):
            return True
        return False

    def __repr__(self) -> str:
        return f'<file {str(self.file_path)}, {self.number}, {"with" if self.has_chinese_subtitle else "without"} subtitle>'  # pragma: no cover

    def __hash__(self) -> int:
        return id(self)
