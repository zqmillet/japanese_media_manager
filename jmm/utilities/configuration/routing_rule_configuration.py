from typing import List
from pydantic import BaseModel
from pydantic import validator

class RoutingRuleConfiguration(BaseModel):
    pattern: str
    crawler_names: List[str]

    @validator('crawler_names')
    def _crawler_names(cls, value: List[str]) -> List[str]:
        if not value:
            raise ValueError('crawler_names is empty')
        return value
