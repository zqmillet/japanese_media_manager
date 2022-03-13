from __future__ import annotations

from pathlib import Path
from typing import List
from typing import Optional
from logging import Logger
from tqdm import tqdm

from jmm.utilities.logger import dumb

class MediaFinder:
    def __init__(self, directories: List[str], recursively: bool = True, minimum_size: int = 0, extensions: Optional[List[str]] = None, logger: Logger = dumb):
        logger.info('scanning media files')
        self.media_paths: List[Path] = []
        extensions = extensions or []

        for directory in directories:
            file_paths = Path(directory).rglob('*') if recursively else Path(directory).glob('*')
            for file_path in file_paths:
                if file_path.suffix not in extensions:
                    continue
                if file_path.stat().st_size < minimum_size:
                    continue
                self.media_paths.append(file_path)

        self.media_paths = sorted(set(self.media_paths))
        self.progress_bar = tqdm(total=len(self.media_paths))

    def __iter__(self) -> MediaFinder:
        self.progress_bar.reset()
        return self

    def __next__(self) -> Path:
        if self.progress_bar.n < len(self.media_paths):
            item = self.media_paths[self.progress_bar.n]
            self.progress_bar.update(1)
            return item
        raise StopIteration
