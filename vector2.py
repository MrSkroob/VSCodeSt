from __future__ import annotations
import random


class Vector3:
    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z

    @property
    def magnitude(self) -> Vector3:
        return (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5

    @property
    def unit(self) -> Vector3:
        if self.x + self.y + self.z == 0:
            return Vector3(0, 0, 0)
        sum_of_axis = self.x + self.y + self.z
        x = self.x / sum_of_axis
        y = self.y / sum_of_axis
        z = self.z / sum_of_axis
        return Vector3(x, y, z)

    def dot(self, vector: Vector3) -> float:
        magnitude0 = self.magnitude
        magnitude1 = vector.magnitude
        return ((self.x * vector.x) + (self.y * vector.y) + (self.z * vector.z)) / (magnitude0 * magnitude1)
    
    def __mul__(self, vector: Vector2) -> Vector2:
        a = (self.x, self.y, 0)
        b = (vector.x, vector.y, 0) # z component is 0 because it's a 2d vector.
        result = [a[1]*b[2] - a[2]*b[1],
            a[2]*b[0] - a[0]*b[2],
            a[0]*b[1] - a[1]*b[0]]
        return Vector3(result[0], result[1], result[2])
    
    def __eq__(self, vector: Vector2):
        return self.x == vector.x and self.y == vector.y and self.z == vector.z

    def __add__(self, vector: Vector3) -> Vector3:
        self.x += vector.x
        self.y += vector.y
        self.z += vector.z
        return self
    
    def __sub__(self, vector: Vector3) -> Vector3:
        self.x -= vector.x
        self.y -= vector.y
        self.z -= vector.z
        return self
    
    def __str__(self) -> str:
        return f"({self.x}, {self.y}, {self.z})"


class Vector2:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    @property
    def magnitude(self) -> Vector2:
        """returns the magnitude of the vector2"""
        return (self.x ** 2 + self.y ** 2) ** 0.5 

    @property
    def unit(self) -> Vector2:
        """returns a normalised unit vector2"""
        if self.x + self.y == 0:
            return Vector2(0, 0)
        sum_of_axis = self.x + self.y
        self.x /= sum_of_axis
        self.y /= sum_of_axis
        return self

    def dot(self, vector: Vector2) -> float:
        """returns dot product between two vector2s"""
        magnitude0 = self.magnitude
        magnitude1 = vector.magnitude
        return ((self.x * vector.x) + (self.y * vector.y)) / (magnitude0 * magnitude1)
    
    def __mul__(self, vector: Vector2) -> Vector3:
        a = (self.x, self.y, 0)
        b = (vector.x, vector.y, 0) # z component is 0 because it's a 2d vector.
        result = [a[1]*b[2] - a[2]*b[1],
            a[2]*b[0] - a[0]*b[2],
            a[0]*b[1] - a[1]*b[0]]
        return Vector3(result[0], result[1], result[2])
    
    def __eq__(self, vector: Vector2):
        return self.x == vector.x and self.y == vector.y

    def __add__(self, vector: Vector2) -> Vector2:
        self.x += vector.x
        self.y += vector.y
        return self

    def __sub__(self, vector: Vector2) -> Vector2:
        self.x -= vector.x
        self.y -= vector.y
        return self

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"


def test():
    test_length = 10
    for _ in range(test_length):
        x = random.randint(-1000, 1000)
        y = random.randint(-1000, 1000)
        x1 = random.randint(-1000, 1000)
        y1 = random.randint(-1000, 1000)
        assert Vector2(x, y) + Vector2(x1, y1) == Vector2(x + x1, y + y1), f"Expected {Vector2(x + x1, y + y1)}, got {Vector2(x, y) + Vector2(x1, y1)}"
    for _ in range(test_length):
        x = random.randint(-1000, 1000)
        y = random.randint(-1000, 1000)
        x1 = random.randint(-1000, 1000)
        y1 = random.randint(-1000, 1000)
        assert Vector2(x, y) - Vector2(x1, y1) == Vector2(x - x1, y - y1), f"Expected {Vector2(x - x1, y - y1)}, got {Vector2(x, y) - Vector2(x1, y1)}"
    for _ in range(test_length):
        x = random.randint(-1000, 1000)
        y = random.randint(-1000, 1000)
        test = Vector2(x, y).unit
        if x == 0 and y == 0:
            assert (test.x + test.y) == 0, f"Expected unit to == 0, got {test.x + test.y}"
        assert 0.99 < (test.x + test.y) < 1.01, f"Expected unit to be around 0.99-1.01, got {test.x + test.y}"
    assert 0.99 < Vector2(10, 0).dot(Vector2(1000000, 0)) < 1.01, f"Expected an answer between 0.99 and 1.01, got {Vector2(1, 0).dot(Vector2(1, 0))}"
    assert Vector2(1, 0) * Vector2(0, 1) == Vector3(0, 0, 1), f"Expected (0, 0, 1), got {Vector2(1, 0) * Vector2(0, 1)}"
    assert Vector2(1, 0) == Vector2(1, 0), "Vectors should equal"
    assert Vector2(0, 1) != Vector2(2, 0), "Vectors should not equal"
    print("ALL TESTS PASSED")


test()
