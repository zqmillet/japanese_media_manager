import typing

from .field import Field
from .list import List

class DataClass:
    def __init__(self, data: dict):
        self._fields = list()
        for key, value in data.items():
            field = getattr(self.__class__, key)

            self._fields.append(key)
            if isinstance(field, List):
                setattr(self, key, [field.item(item) for item in value])
                continue

            if not isinstance(value, field.type):
                raise TypeError()

            setattr(self, key, value)

    def __repr__(self):
        fields = ['='.join([field, repr(getattr(self, field))]) for field in self._fields]
        return f'{self.__class__.__name__}({", ".join(fields)})'
