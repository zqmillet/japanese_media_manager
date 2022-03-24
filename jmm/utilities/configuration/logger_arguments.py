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

    def dict(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:  # pylint: disable=unused-argument
        return {key: value for key, value in self._iter() if value is not None}
