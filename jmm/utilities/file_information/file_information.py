from typing import Optional
from pathlib import Path

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
        return f'<file {str(self.file_path)}, {self.number}, {"with" if self.has_chinese_subtitle else "without"} subtitle>'
