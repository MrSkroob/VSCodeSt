from __future__ import annotations


class Node():
    def __init__(self, data, next_node: Node) -> None:
        self._data = data
        self._next_node = next_node
    
    @property
    def data(self):
        return self._data

    def get_next_node(self):
        return self._next_node
    
    def __str__(self):
        return str(self._data)


class Stack():
    def __init__(self) -> None:
        self._size = 0
        self._bottom = 0
        self._head_node = None
        self._stack = []

    @property
    def size(self):
        return self._size
    
    def push(self, data):
        if self._size == 0:
            node = Node(data, None)
        else:
            node = Node(data, self._stack[0])
        self._head_node = node
        self._stack.insert(0, node)
        self._size += 1
    
    def pop(self):
        if self._size == self._bottom:
            raise IndexError("Stack is empty")
        node: Node = self._stack.pop(0)
        self._head_node = node.get_next_node()
        self._size -= 1
        return node.data

    def get_stack(self):
        return self._stack

    def peak(self):
        return self._head_node
    
    def isempty(self):
        return self._size == self._bottom


new_stack = Stack()
new_stack.push("hello")
new_stack.push("world")
new_stack.push("!")


print(new_stack.get_stack())


for i in new_stack.get_stack():
    print(i.data, i.get_next_node())


print("--------------------")
new_stack.pop()
new_stack.push("goodbye")


for i in new_stack.get_stack():
    print(i.data, i.get_next_node())