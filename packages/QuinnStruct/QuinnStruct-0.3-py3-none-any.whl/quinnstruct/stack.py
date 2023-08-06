import sys
from .linklist import LinkList


# ********************************
class Stack():

    _data = None

    def __init__(self):
        self._data = LinkList()

    def count(self) -> int:
        return self._data.count()

    def pop(self) -> object:
        b, val = self._data.peekHead()
        if b:
            self._data.remove(val)
        return val

    def push(self, val: object) -> bool:
        self._data.insert(val)
        return True

    def peek(self) -> [bool, object]:
        return self._data.peekHead()

