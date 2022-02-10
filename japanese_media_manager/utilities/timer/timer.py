import time as _time

class Timer():

    def __init__(self):
        self.start_time = 0
        self.end_time = 0
        self.time = 0

    def __enter__(self):
        self.start_time = _time.time()
        return self

    def __exit__(self, exception_type, value, trace):
        self.end_time = _time.time()
        self.time = self.end_time - self.start_time
