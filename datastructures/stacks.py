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
        return self.stack[self.pointer - 1]
    
    def isempty(self):
        return self.pointer == self.bottom
    
    def isfull(self):
        return self.pointer == self.max


new_stack = Stack(10)


for i in range(10):
    new_stack.push(i)


new_stack.pop()
# print(new_stack.peak())
# print(new_stack.isempty())
# print(new_stack.isfull())
# print(new_stack.stack)


class Queue():
    def __init__(self, size) -> None:
        self.front = -1
        self.rear = -1
        self.queue = {}
        self.size = size
    
    def add(self, item):
        if self.front == -1 and self.rear == -1:
            self.front = 0
            self.rear = 0
            self.queue[self.rear] = item
        elif (self.rear + 1) % self.size == self.front:
            raise IndexError("Queue full")
        else:
            self.rear = (self.rear + 1) % self.size
            self.queue[self.rear] = item
    
    def pop(self):
        if self.front == -1 and self.rear == -1:
            raise IndexError("Queue empty")
        else:
            del self.queue[self.front]
            if self.front == self.rear:
                self.front = -1
                self.rear = -1
            else:
                self.front = (self.front + 1) % self.size

    def isempty(self):
        return self.front == -1 and self.rear == -1
    
    def isfull(self):
        return (self.rear + 1) % self.size == self.front


new_queue = Queue(10)
for i in range(10):
    new_queue.add(i)


print(new_queue.queue)
new_queue.pop()
new_queue.pop()


print(new_queue.queue)

new_queue.add(0)
new_queue.add(0)

print(new_queue.isfull())

print(new_queue.queue)