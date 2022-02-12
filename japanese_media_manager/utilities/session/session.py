import time
import urllib3
import requests

class Session(requests.Session):
    def __init__(self, *args, interval=1, timeout=None, proxies=None, retries=3, **kwargs):
        self.interval = interval
        self.timeout = timeout

        super().__init__(*args, **kwargs)
        self.proxies.update(proxies or {'http': None, 'https': None})
        self.last_access_time = 0

        adapter = requests.adapters.HTTPAdapter(
            max_retries=urllib3.util.Retry(
                total=retries,
                allowed_methods=['GET', 'POST'],
                status_forcelist=[500]
            )
        )

        self.mount('https://', adapter)
        self.mount('http://', adapter)

    def request(self, *args, **kwargs):
        time.sleep(max(0, self.interval - time.time() + self.last_access_time))
        self.last_access_time = time.time()
        return super().request(*args, **kwargs, timeout=self.timeout)
