class Rectangle():
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    def get_area(self):
        return self.width * self.height

    def get_perimeter(self):
        return self.width * 2 + self.height * 2

    def get_diagonal(self):
        return pow(pow(self.width, 2) + pow(self.height, 2), 0.5)


a_boxy_boy = Rectangle(4**12387, 3*9812)
print(a_boxy_boy.get_area())