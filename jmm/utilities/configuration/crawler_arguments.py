from typing import Dict
from typing import Any
from typing import Optional
from pydantic import BaseModel
from pydantic import StrictStr
from pydantic import Field
from pydantic import Extra

from .proxies import Proxies

class CrawlerArguments(BaseModel, extra=Extra.forbid):
    base_url: Optional[StrictStr] = None
    interval: float = Field(default=0, ge=0)
    timeout: Optional[float] = 1
    proxies: Optional[Proxies] = None
    retries: int = Field(default=3, ge=0)
    verify: bool = False

    def dict(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:  # pylint: disable=unused-argument
        return {key: value for key, value in self._iter() if value is not None}
