from typing import Optional
from pydantic import BaseModel
from pydantic import StrictStr

class TranslatorArguments(BaseModel):
    app_id: Optional[StrictStr]
    app_key: Optional[StrictStr]
