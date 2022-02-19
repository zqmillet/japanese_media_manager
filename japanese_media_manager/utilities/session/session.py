import time
import http
import typing
import urllib3
import requests

def get_retry_class(interval: float) -> type:
    class Retry(urllib3.util.Retry):
        def sleep(self, response: urllib3.response.HTTPResponse = None) -> None:
            time.sleep(interval)
    return Retry

class Session(requests.Session):
    def __init__(
        self,
        *args: typing.Any,
        interval: float = 0,
        timeout: typing.Optional[float] = None,
        proxies: typing.Optional[dict] = None,
        retries: int = 3,
        identity: str = None,
        verify: bool = False,
        **kwargs: typing.Any
    ):
        super().__init__(*args, **kwargs)
        self.interval = interval
        self.timeout = timeout
        self.identity = identity
        self.verify = verify
        self.proxies.update(proxies or {'http': None, 'https': None})
        self.last_access_time = 0.0

        for prefix in ['http://', 'https://']:
            self.mount(
                prefix=prefix,
                adapter=requests.adapters.HTTPAdapter(
                    max_retries=get_retry_class(interval)(
                        total=retries,
                        allowed_methods=["HEAD", "GET", "POST", "PUT", "DELETE", "OPTIONS", "TRACE"],
                        status_forcelist=[
                            http.HTTPStatus.BAD_GATEWAY,
                            http.HTTPStatus.BAD_REQUEST,
                            http.HTTPStatus.INTERNAL_SERVER_ERROR,
                            http.HTTPStatus.FORBIDDEN,
                        ],
                    )
                )
            )

    def request(self, *args: typing.Any, **kwargs: typing.Any) -> requests.models.Response:
        time.sleep(max(0, self.interval - time.time() + self.last_access_time))
        self.last_access_time = time.time()
        kwargs['timeout'] = kwargs.get('timeout') or self.timeout
        kwargs['verify'] = kwargs.get('verify') or self.verify
        return super().request(*args, **kwargs)
