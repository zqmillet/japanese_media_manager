from .null import Null

class List:
    def __init__(self, item, alias=None, default=Null()):
        self.item = item
        self.alias = alias
        self.default = default
