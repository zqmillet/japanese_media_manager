import time
import http
from typing import Optional
from typing import Any
from requests import Session as _Session
from requests import adapters
from requests import models
from urllib3 import disable_warnings
from urllib3 import exceptions
from urllib3 import util
from urllib3 import response as _response
from pydantic import BaseModel

disable_warnings(exceptions.InsecureRequestWarning)

class Proxies(BaseModel):
    http: Optional[str] = None
    https: Optional[str] = None

def get_retry_class(interval: float) -> type:
    class Retry(util.Retry):
        def sleep(self, response: _response.HTTPResponse = None) -> None:
            time.sleep(interval)
    return Retry

class Session(_Session):
    """
    a request session of crawler.
    """
    def __init__(
        self,
        *args: Any,
        interval: float = 0,
        timeout: Optional[float] = None,
        proxies: Optional[Proxies] = None,
        retries: int = 3,
        verify: bool = False,
        **kwargs: Any
    ):
        """
        :param interval: 该会话请求的最小间隔, 单位(秒), 对于某些网站, 需要设置此参数, 防止被封 IP 地址.
        :param timeout: 该会话请求的超时时间, 其默认时间为 :py:mod:`requests` 库中设置的默认时间. 通常情况下, 这个时间都是非常长的, 如果遇到网络问题, 会导致整个爬虫线程阻塞, 建议设置该参数, 防止线程阻塞.
        :param proxies: 如果需要代理才能访问, 需要设置此参数, 默认情况下不走代理.
        :param retries: 对于每一个请求的最大重试次数. 当某次请求出现异常时, 需要进行 3 次重试, 你可以通过设定这个参数来修改重试的次数. 注意, 重试也会受 :py:obj:`interval` 参数的影响, 而不会立即重试.
        :param verify: 需要设置此参数为 HTTPS 请求验证 SSL 证书, 默认为不验证.
        """
        super().__init__(*args, **kwargs)
        self.interval = interval
        self.timeout = timeout
        self.verify = verify
        self.proxies.update(proxies.dict() if proxies else {})
        self.last_access_time = 0.0

        for prefix in ['http://', 'https://']:
            self.mount(
                prefix=prefix,
                adapter=adapters.HTTPAdapter(
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

    def request(self, *args: Any, **kwargs: Any) -> models.Response:
        time.sleep(max(0, self.interval - time.time() + self.last_access_time))
        self.last_access_time = time.time()
        kwargs['timeout'] = kwargs.get('timeout') or self.timeout
        kwargs['verify'] = kwargs.get('verify') or self.verify
        return super().request(*args, **kwargs)
