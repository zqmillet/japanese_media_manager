from typing import List
from pydantic import BaseModel
from pydantic import Field

class MediaFinderArguments(BaseModel):
    directories: List[str]
    recursively: bool
    minimum_size: int = Field(ge=0)
    extensions: List[str]
