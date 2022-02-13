import time
import http
import urllib3
import requests

def get_retry_class(interval):
    class Retry(urllib3.util.Retry):
        def sleep(self, response=None):
            time.sleep(interval)
    return Retry

class Session(requests.Session):
    instances = {}

    def __new__(cls, *args, **kwargs): # pylint: disable=unused-argument
        identity = kwargs.get('identity')
        if identity not in Session.instances:
            Session.instances[identity] = super().__new__(cls)
        return Session.instances[identity]

    def __init__(self, *args, interval=0, timeout=None, proxies=None, retries=3, identity=None, session_initialization=None, **kwargs):
        self.interval = interval
        self.timeout = timeout
        self.identity = identity

        super().__init__(*args, **kwargs)
        self.proxies.update(proxies or {'http': None, 'https': None})
        self.last_access_time = 0

        retry = get_retry_class(interval)(
            total=retries,
            allowed_methods=["HEAD", "GET", "POST", "PUT", "DELETE", "OPTIONS", "TRACE"],
            status_forcelist=[
                http.HTTPStatus.BAD_GATEWAY,
                http.HTTPStatus.BAD_REQUEST,
                http.HTTPStatus.INTERNAL_SERVER_ERROR,
                http.HTTPStatus.FORBIDDEN,
            ],
        )

        adapter = requests.adapters.HTTPAdapter(max_retries=retry)

        self.mount('https://', adapter)
        self.mount('http://', adapter)

        if session_initialization:
            session_initialization['call'](self, *session_initialization.get('args'))

    def request(self, *args, **kwargs):
        time.sleep(max(0, self.interval - time.time() + self.last_access_time))
        self.last_access_time = time.time()
        kwargs['timeout'] = kwargs.get('timeout') or self.timeout
        return super().request(*args, **kwargs)
