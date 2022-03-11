from logging import Logger as BaseLogger
from logging import DEBUG
from logging import StreamHandler
from logging import FileHandler
from logging import Formatter
from typing import Optional

class Logger(BaseLogger):
    """
    Python 内置类 :py:class:`logging.Logger` 的二次封装, 牺牲灵活性, 提升易用性.
    """
    def __init__(self, name: str = 'jmm', level: int = DEBUG, file_path: Optional[str] = None, fmt: str = '%(asctime)s | %(name)s | %(levelname)-8s | %(message)s'):
        """
        :param name: 日志的名称.
        :param level: 日志的最低级别.
        :param file_path: 日志的路径, 如果指定该参数, 则会向该文件以及控制台同时输出日志, 如果不指定该参数, 只会在控制台中输出日志.
        :param fmt: 日志的格式.
        """

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
