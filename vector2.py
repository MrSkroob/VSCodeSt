from __future__ import annotations


class Vector2:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    @property
    def magnitude(self) -> Vector2:
        """returns the magnitude of the vector"""
        return (self.x ** 2 + self.y **2) ** 0.5 

    @property
    def unit(self) -> Vector2:
        """should actually be called normalise, but I'm used to it being called unit"""
        if self.x + self.y == 0:
            return Vector2(0, 0)
        x = self.x / (self.x + self.y)
        y = self.y / (self.x + self.y)
        return Vector2(x, y)

    def dot(self, vector: Vector2) -> float:
        """returns dot product between two vectors"""
        magnitude0 = self.magnitude
        magnitude1 = vector.magnitude
        return ((self.x * vector.x) + (self.y * vector.y)) / (magnitude0 * magnitude1)

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


vector = Vector2(1, 1)
vector1 = Vector2(0, 1)
print(vector.unit)
print(vector1.unit)
print((vector + vector1).unit)