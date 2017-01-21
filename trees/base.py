from collections import Sequence
from typing import Any, Tuple, Union
from weakref import WeakKeyDictionary


class NodePtrDescriptor(object):
    def __init__(self):
        self._values = WeakKeyDictionary()

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self._values.get(instance, None)

    def __set__(self, instance, value):
        self._values[instance] = value


class BinaryNode(Sequence):
    parent = NodePtrDescriptor()
    left = NodePtrDescriptor()
    right = NodePtrDescriptor()

    def __init__(self, data: Any, parent: "BinaryNode" = None,
                 left: "BinaryNode" = None, right: "BinaryNode" = None) -> None:
        self.data = data
        self.left = left
        self.right = right
        self.parent = parent

    def _search(self, count, index) -> Tuple["BinaryNode", int]:
        found = None
        if count == index:
            return self, count
        if self.left:
            (found, count) = self.left._search(count + 1, index)
        if not found and (not index or count < index) and self.right:
            (found, count) = self.right._search(count + 1, index)
        return found, count + 1

    def __getitem__(self, item):
        found, _ = self._search(0, item)
        if not found:
            raise IndexError('Index out of range')
        return found.data

    def __len__(self):
        _, count = self._search(0, None)
        return count

    def __repr__(self):
        return "Node({0})".format(self.data)


class BinarySearchTree(Sequence):
    def __init__(self, value):
        self.root = BinaryNode(value)

    def __len__(self):
        return len(self.root)

    def __getitem__(self, item):
        return self.root[item]

    def tree_minimum(self, bin_node: BinaryNode = None) -> BinaryNode:
        if not bin_node:
            bin_node = self.root  # type: BinaryNode
        while bin_node.left is not None:
            bin_node = bin_node.left
        return bin_node

    def tree_maximum(self, bin_node: BinaryNode = None) -> BinaryNode:
        if not bin_node:
            bin_node = self.root  # type: BinaryNode
        while bin_node.right is not None:
            bin_node = bin_node.right
        return bin_node

    def tree_search(self, to_search: int) -> BinaryNode:

        def recurse(bin_node: BinaryNode, value: int) -> Union[BinaryNode, None]:
            if bin_node is None or value == bin_node.data:
                return bin_node
            if value < bin_node.data:
                return recurse(bin_node.left, value)
            else:
                return recurse(bin_node.right, value)

        return recurse(self.root, to_search)

    def in_order_tree_walk(self) -> None:

        def recurse(bin_node: BinaryNode) -> None:
            if bin_node is not None:
                recurse(bin_node.left)
                print(bin_node)
                recurse(bin_node.right)

        recurse(self.root)

    def tree_successor(self, bin_node: BinaryNode):
        if bin_node.right is not None:
            return self.tree_minimum(bin_node)
        parent = bin_node.parent
        while parent and bin_node == parent.right:
            bin_node = parent
            parent = parent.parent
        return parent

    def tree_predecessor(self, bin_node: BinaryNode):
        if bin_node.left is not None:
            return self.tree_maximum(bin_node)
        parent = bin_node.parent
        while parent and bin_node == parent.left:
            bin_node = parent
            parent = parent.parent
        return parent
