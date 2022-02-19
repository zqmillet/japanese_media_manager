from __future__ import annotations
from time import time
from typing import Any

class Timer:
    def __init__(self) -> None:
        self.start_time = 0.0
        self.end_time = 0.0
        self.time = 0.0

    def __enter__(self) -> Timer:
        self.start_time = time()
        return self

    def __exit__(self, exception_type: type, value: Exception, trace: Any) -> None:
        self.end_time = time()
        self.time = self.end_time - self.start_time
