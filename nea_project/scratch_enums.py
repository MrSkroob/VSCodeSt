from enum import Enum


class Coordinates:
    def __init__(self, x: int | float, y: int | float) -> None:
        self.x = x
        self.y = y


class Position(Enum):
    RANDOM_POSITION = 0
    MOUSE_POINTER = 1


class RotationStyle(Enum):
    LEFT_RIGHT = 0
    DONT_ROTATE = 1
    ALL_AROUND = 2
