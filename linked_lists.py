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


class StackIterator():
    """Iterator class for stacks"""
    def __init__(self, stack: Stack) -> None:
        self._stack = stack
        self._current_node = stack._head_node
    
    def __next__(self):
        """Returns the next node"""
        self._current_node = self._current_node.get_next_node()
        if self._current_node is None:
            raise StopIteration
        return self._current_node


class Stack():
    def __init__(self) -> None:
        self._size = 0
        self._bottom = 0
        self._head_node = None

    @property
    def size(self):
        return self._size
    
    def push(self, data):
        if self._size == 0:
            node = Node(data, None)
        else:
            node = Node(data, self._head_node)
        self._head_node = node
        self._size += 1
    
    def pop(self):
        if self._size == self._bottom:
            raise IndexError("Stack is empty")
        node = self._head_node
        self._head_node = node.get_next_node()
        self._size -= 1
        return node.data

    def peak(self):
        return self._head_node
    
    def isempty(self):
        return self._size == self._bottom

    def __iter__(self):
        return StackIterator(self)
    
    def __str__(self):
        if self._size == 0:
            return ""
        node = self._head_node
        string = "["
        for i in range(self._size):
            if i == self._size - 1:
                string += node.data + "]"
            else:
                string += node.data + ", "
            node = node.get_next_node()
        return string


new_stack = Stack()
new_stack.push("hello")
new_stack.push("world")
new_stack.push("!")
print(new_stack)
print(new_stack.peak())


print("--------------------")
new_stack.pop()
new_stack.push("goodbye")
print(new_stack)
print(new_stack.peak())

print("--------------------")
for i in new_stack:
    print(i)