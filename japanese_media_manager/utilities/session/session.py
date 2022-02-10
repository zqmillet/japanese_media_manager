import time
import requests

class Session(requests.Session):
    def __init__(self, *args, interval=1, **kwargs):
        self.interval = interval
        super().__init__(*args, **kwargs)

        self.last_access_time = 0

    def get(self, *args, **kwargs):
        time.sleep(max(0, self.interval - time.time() + self.last_access_time))
        self.last_access_time = time.time()

        return super().get(*args, **kwargs)
