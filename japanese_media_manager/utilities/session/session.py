import time
import functools
import requests

class Session(requests.Session):
    def __init__(self, *args, interval=1, **kwargs):
        self.interval = interval
        super().__init__(*args, **kwargs)
        for method_name in ['get', 'post', 'patch', 'put', 'delete']:
            setattr(self, method_name, self.wrap(method_name))
        self.last_access_time = 0

    def wrap(self, method_name):
        method = getattr(self, method_name)

        @functools.wraps(method)
        def _method(*args, **kwargs):
            time.sleep(max(0, self.interval - time.time() + self.last_access_time))
            self.last_access_time = time.time()
            return method(*args, **kwargs)

        return _method
