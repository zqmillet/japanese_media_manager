from __future__ import annotations

from pathlib import Path
from typing import List
from typing import Optional
from logging import Logger
from tqdm import tqdm

from jmm.utilities.logger import dumb
from jmm.utilities.functions import get_number

class FileInformation:
    def __init__(self, file_path: Path):
        self.file_path = file_path

    @property
    def number(self) -> Optional[str]:
        return get_number(self.file_path.name)

    @property
    def has_chinese_subtitle(self) -> bool:
        return self.file_path.name.lower().endswith('-c')

    def __repr__(self) -> str:
        return f'<file {str(self.file_path)}, self.number, {self.has_chinese_subtitle}>'

class MediaFinder:
    def __init__(self, directories: List[str], recursively: bool = True, minimum_size: int = 0, extensions: Optional[List[str]] = None, logger: Logger = dumb):
        logger.info('scanning media files')
        self.media_paths: List[Path] = []
        self.extensions: List[str] = list(map(lambda x: x.lower(), extensions or []))
        self.directories: List[str] = directories
        self.recursively: bool = recursively
        self.progress_bar = tqdm(total=len(self.media_paths))
        self.minimum_size = minimum_size

    def __iter__(self) -> MediaFinder:
        for directory in self.directories:
            file_paths = Path(directory).rglob('*') if self.recursively else Path(directory).glob('*')
            for file_path in file_paths:
                if not file_path.is_file():
                    continue
                if file_path.suffix.lower() not in self.extensions:
                    continue
                if file_path.stat().st_size < self.minimum_size:
                    continue
                self.media_paths.append(file_path)

        self.media_paths = sorted(set(self.media_paths))
        self.progress_bar = tqdm(total=len(self.media_paths))
        self.progress_bar.reset()

        return self

    def __next__(self) -> FileInformation:
        if self.progress_bar.n < len(self.media_paths):
            item = self.media_paths[self.progress_bar.n]
            self.progress_bar.update(1)
            return FileInformation(item)
        raise StopIteration
