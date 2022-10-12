from __future__ import annotations


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
        x = self.x / sum_of_axis
        y = self.y / sum_of_axis
        return Vector2(x, y)

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


vector2a = Vector2(1, 1)
vector2b = Vector2(1, 0)

print((vector2a * vector2b).unit) # this will become a vector3 because vector2s can't give a cross product.

vector3a = Vector3(1, 0, 3)
vector3b = Vector3(4, 5, 1)
print(vector3a.magnitude)
print(vector3b.magnitude)

print(vector3a.unit)
print(vector3b.unit)
print((vector3a * vector3b).unit)
print(vector3a - vector3b)
print(vector3a + vector3b)