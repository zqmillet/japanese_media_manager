from .field import Field
from .null import Null
from .list import List
from .exceptions import TypeMissMatchException
from .exceptions import FieldMissException
from .exceptions import AssertionException

class DataClass:
    def __init__(self, data: dict, name='data'):
        self._fields = self.__get_fields__()

        for field in self._fields:
            sub_name = name + f'[{repr(field.alias)}]'
            value = data.get(field.alias, field.default)

            if isinstance(value, Null):
                raise FieldMissException(data, field, name)

            if isinstance(field, List):
                setattr(self, field.alias, [field.item(item, name=sub_name + f'[{index}]') for index, item in enumerate(value)])
                continue

            if issubclass(field.type, DataClass):
                setattr(self, field.alias, field.type(value, name=sub_name))
                continue

            if not isinstance(value, field.type):
                raise TypeMissMatchException(value, field, sub_name)

            if not field.assertion(value):
                raise AssertionException(value, field, sub_name)

            setattr(self, field.alias, value)

    def __get_fields__(self):
        fields = []
        for key in dir(self):
            if key.startswith('_'):
                continue

            value = getattr(self, key)

            if isinstance(value, (Field, List)):
                value.alias = value.alias or key
                fields.append(value)
        return fields

    def __repr__(self):
        fields = ['='.join([field.alias, repr(getattr(self, field.alias))]) for field in self._fields]
        return f'{self.__class__.__name__}({", ".join(fields)})'
