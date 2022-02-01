import typing

from .field import Field
from .list import List
from .exceptions import TypeMissMatchException

class DataClass:
    def __init__(self, data: dict, name='data'):
        self._fields = list()
        for key, value in data.items():
            sub_name = name + f'[{repr(key)}]'

            field = getattr(self.__class__, key)

            self._fields.append(key)
            if isinstance(field, List):
                setattr(self, key, [field.item(item, name=sub_name + f'[{index}]') for index, item in enumerate(value)])
                continue

            if issubclass(field.type, DataClass):
                setattr(self, key, field.type(value, name=sub_name))
                continue

            if not isinstance(value, field.type):
                raise TypeMissMatchException(value, field, sub_name)

            setattr(self, key, value)

    def __repr__(self):
        fields = ['='.join([field, repr(getattr(self, field))]) for field in self._fields]
        return f'{self.__class__.__name__}({", ".join(fields)})'
