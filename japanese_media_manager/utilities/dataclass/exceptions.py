class DataClassException(Exception):
    pass

class TypeMissMatchException(DataClassException):
    def __init__(self, value, field, name):
        super().__init__(f'{name} = {repr(value)}, but its type should be {field.type.__name__}')
