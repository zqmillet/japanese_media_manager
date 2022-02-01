class DataClassException(Exception):
    pass

class TypeMissMatchException(DataClassException):
    def __init__(self, value, field, name):
        super().__init__(f'{name} = {repr(value)}, but its type should be {field.type.__name__}')

class FieldMissException(DataClassException):
    def __init__(self, data, field, name):
        super().__init__(f'cannot find field {field.alias} in {name} = {repr(data)}')

class AssertionException(DataClassException):
    def __init__(self, value, field, name):
        super().__init__(f'{name} = {repr(value)} cannot pass assertion = {repr(field.assertion)}')
