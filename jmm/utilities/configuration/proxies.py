from typing import Optional
from pydantic import BaseModel

class Proxies(BaseModel):
    http: Optional[str]
    https: Optional[str]
