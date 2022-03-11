from __future__ import annotations
from time import time
from typing import Any

class Timer:
    """
    计时上下文管理器, 仅供自动化测试使用.

    .. code-block:: python

        with Timer() as timer:
            # some code
        print('consuming time is', timer.time)
    """

    def __init__(self) -> None:
        """
        构造时无需任何参数.
        """
        self.start_time = 0.0
        self.end_time = 0.0
        self.time = 0.0

    def __enter__(self) -> Timer:
        self.start_time = time()
        return self

    def __exit__(self, exception_type: type, value: Exception, trace: Any) -> None:
        self.end_time = time()
        self.time = self.end_time - self.start_time
