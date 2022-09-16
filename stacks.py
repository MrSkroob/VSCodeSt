class Stack():
    def __init__(self, size: int) -> None:
        self.max = size
        self.pointer = 0
        self.bottom = 0
        self.stack = []
    
    def push(self, item):
        if self.pointer == self.max:
            raise IndexError("Stack is full")
        self.stack.append(item)
        self.pointer += 1
    
    def pop(self):
        if self.pointer == self.bottom:
            raise IndexError("Stack is empty")
        self.stack.pop()
        self.pointer -= 1
    
    def peak(self):
        return self.stack[0]
    
    def isempty(self):
        return self.pointer == self.bottom
    
    def isfull(self):
        return self.pointer == self.max


new_stack = Stack(10)


for i in range(10):
    new_stack.push(i)


new_stack.pop()
print(new_stack.peak())
print(new_stack.isempty())
print(new_stack.isfull())
print(new_stack.stack)
