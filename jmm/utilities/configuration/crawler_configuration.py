from typing import Type
from pydoc import locate
from pydantic import BaseModel
from pydantic import Field
from pydantic import validator

from jmm.crawlers.base import Base

from .crawler_arguments import CrawlerArguments

class CrawlerConfiguration(BaseModel):
    name: str
    clazz: Type[Base] = Field(alias='class')
    arguments: CrawlerArguments = Field(alias='with', default=CrawlerArguments())

    @validator('clazz', always=True, pre=True)
    def _clazz(cls, value: str) -> Type[Base]:
        clazz = locate(value)
        if not clazz:
            raise ValueError(f'cannot get class from {repr(value)}')
        if not isinstance(clazz, type):
            raise ValueError(f'class {repr(value)} must be a type')
        if clazz is Base:
            raise ValueError(f'class cannot be {Base.__module__}.{Base.__name__}')
        class_name = clazz.__name__
        if not issubclass(clazz, Base):
            raise ValueError(f'class {repr(class_name)} must be a subclass of class {Base.__module__}.{Base.__name__}')
        return clazz
