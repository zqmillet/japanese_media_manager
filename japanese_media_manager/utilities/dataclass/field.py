from .null import Null

class Field:
    def __init__(self, type=None, alias=None, assertion=lambda x: True, default=Null()):
        self.type = type or object
        self.alias = alias
        self.assertion = assertion
        self.default = default

    def __repr__(self):
        return f'<field {self.alias} {self.type.__name__}>'
