from logging import Logger as BaseLogger
from logging import DEBUG
from logging import StreamHandler
from logging import FileHandler
from logging import Formatter
from typing import Optional

class Logger(BaseLogger):
    def __init__(self, name: str = 'jmm', level: int = DEBUG, file_path: Optional[str] = None, fmt: str = '%(asctime)s | %(name)s | %(levelname)-8s | %(message)s'):
        super().__init__(name)
        self.setLevel(level)

        stream_handler = StreamHandler()
        stream_handler.setLevel(level)
        stream_handler.setFormatter(Formatter(fmt))
        self.addHandler(stream_handler)

        if not file_path:
            return

        file_handler = FileHandler(filename=file_path)
        file_handler.setLevel(level)
        file_handler.setFormatter(Formatter(fmt))
        self.addHandler(file_handler)
