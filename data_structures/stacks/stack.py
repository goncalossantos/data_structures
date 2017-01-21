from typing import Any
from chapter_2.linked_list import Node


class PopEmpty(Exception):
    pass


class StackNode(Node):
    def __init__(self, value):
        self.before = None
        super(StackNode, self).__init__(value)


class Stack(object):
    def __init__(self):
        self._top = None
        self._length = 0

    def push(self, value: Any) -> None:
        new_node = StackNode(value)
        if self._top:
            self._top.before = new_node
        new_node.next = self._top
        self._top = new_node
        self._length += 1

    def pop(self) -> Any:
        if not self._top:
            raise PopEmpty
        value = self._top.value
        self._length -= 1
        self._top = self._top.next

        if self._top:
            self._top.before = None

        return value

    def is_empty(self):
        return True if self._length == 0 else False

    def __len__(self):
        return self._length

    def peek(self) -> Any:
        return None if not self._top else self._top.value
