from __future__ import annotations
import random


class Node():
    def __init__(self, data, right_node=None, left_node=None) -> None:
        self._data = data
        self._left_node: Node = -1  # type: ignore
        self._right_node: Node = -1  # type: ignore
        if left_node is not None:
            self._left_node = left_node
        if right_node is not None:
            self._right_node = right_node

    def set_node(self, node: Node):
        if node._data > self._data:
            right_node = self._right_node
            if right_node == -1:
                self._right_node = node
                return
            else:
                return right_node.set_node(node)
        else:
            left_node = self._left_node
            if left_node == -1:
                self._left_node = node
                return
            else:
                return left_node.set_node(node)

    def print_tree(self):
        if self._left_node != -1:
            self._left_node.print_tree()
        if self._right_node != -1:
            self._right_node.print_tree()

    def set_right_node(self, node: Node):
        self._right_node = node
    
    def set_left_node(self, node: Node):
        self._left_node = node

    def get_right_node(self) -> Node:
        return self._right_node
    
    def get_left_node(self) -> Node:
        return self._left_node

    def get_data(self):
        return self._data


def create_tree(tree: list):
    first_node = Node(tree[0])
    for i in range(1, len(tree)):
        first_node.set_node(Node(tree[i]))
    return first_node


def is_in_tree(first_node: Node, item):
    if first_node.get_data() == item:
        return True
    if first_node.get_data() < item:
        right_node = first_node.get_right_node()
        if right_node == -1:
            return False
        if right_node.get_data() != item:
            return is_in_tree(right_node, item)
        else:
            return True
    else:
        left_node = first_node.get_left_node()
        if left_node == -1:
            return False
        if left_node.get_data() != item:
            return is_in_tree(left_node, item)
        else:
            return True


tree_set = []
for i in range(0, 100):
    tree_set.append(random.randint(0, 100))

tree = create_tree(tree_set)
tree.print_tree()
for i in range(100):
    bool1 = is_in_tree(tree, i)
    bool2 = i in tree_set
    assert bool1 == bool2, f"{i}, {bool2}, {tree_set}"
