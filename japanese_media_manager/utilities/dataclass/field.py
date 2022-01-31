class Field:
    def __init__(self, type=None, alias=None, assertion=None):
        self.type = type or object
        self.alias = alias
        self.assertion = assertion
