from typing import Any
from typing import Dict
from typing import Optional
from pydantic import BaseModel

from .proxies import Proxies

class CrawlerArguments(BaseModel):
    base_url: Optional[str] = None
    interval: float = 0
    timeout: Optional[float] = None
    proxies: Optional[Proxies] = None
    retries: int = 3
    verify: bool = False

    def dict(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:  # pylint: disable=unused-argument
        return {key: value for key, value in self._iter() if value is not None}
