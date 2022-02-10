import requests

class Session(requests.Session):
    def __init__(self, *args, interval=1, **kwargs):
        self.interval = interval
        super().__init__(*args, **kwargs)
