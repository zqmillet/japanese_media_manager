from pathlib import Path
from typing import List
from typing import Optional
from logging import Logger

from jmm.utilities.logger import dumb

def get_file_paths(directories: List[str], recursively: bool = True, minimum_size: int = 0, extensions: Optional[List[str]] = None, logger: Logger = dumb) -> List[Path]:
    logger.info('scanning media files')
    media_paths = []
    extensions = list(map(lambda x: x.lower(), extensions or []))

    for directory in directories:
        file_paths = Path(directory).rglob('*') if recursively else Path(directory).glob('*')
        for file_path in file_paths:
            if not file_path.is_file():
                continue
            if file_path.suffix.lower() not in extensions:
                continue
            if file_path.stat().st_size < minimum_size:
                continue
            media_paths.append(file_path)

    return sorted(set(media_paths))
