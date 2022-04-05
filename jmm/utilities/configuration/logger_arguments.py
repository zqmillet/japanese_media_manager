from typing import Optional
from typing import Dict
from typing import Any
from pydantic import BaseModel
from pydantic import StrictInt
from pydantic import StrictStr

class LoggerArguments(BaseModel):
    name: Optional[StrictStr]
    level: Optional[StrictInt]
    file_path: Optional[StrictStr]
    fmt: Optional[StrictStr]

    def dict(self, *_: Any, **__: Any) -> Dict[str, Any]:
        return {key: value for key, value in self._iter() if value is not None}
