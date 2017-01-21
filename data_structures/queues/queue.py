from typing import Any
from data_structures.linked_lists.linked_list import Node


class PopEmpty(Exception):
    pass


class Queue(object):
    def __init__(self):
        self._head = self._tail = None
        self._length = 0

    def enqueue(self, value: Any) -> None:
        new_node = Node(value)
        if not self._tail:
            self._tail = new_node
        if self._head:
            self._head.next = new_node

        self._head = new_node
        self._length += 1

    def deque(self) -> Any:
        if not self._tail:
            raise PopEmpty
        value = self._tail.value
        self._length -= 1

        if self._head == self._tail:
            self._head = self._tail = self._tail.next
        else:
            self._tail = self._tail.next

        return value

    def is_empty(self):
        return True if self._length == 0 else False

    def __len__(self):
        return self._length
