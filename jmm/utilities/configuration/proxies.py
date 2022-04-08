from typing import Optional
from pydantic import BaseModel
from pydantic import Extra
from pydantic import StrictStr

class Proxies(BaseModel, extra=Extra.forbid):
    http: Optional[StrictStr] = None
    https: Optional[StrictStr] = None

    def __bool__(self) -> bool:
        return any([self.http, self.https])
