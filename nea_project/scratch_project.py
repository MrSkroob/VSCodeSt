from __future__ import annotations
import scratch_enums


class BaseScripts():
    # events
    def green_flag_clicked(self, code: function, *args, **kwargs):
        code(args, kwargs)
    
    # looks
    def switch_costume_to(self, costume: int | str):
        pass


class Sprite(BaseScripts):
    # motion blocks
    def __init__(self, name: str) -> None:
        self.name = name
    def move(self, steps: int | float):
        pass
    def turn_left(self, degrees: int | float):
        pass
    def turn_right(self, degrees: int | float):
        pass
    def goto(self, position: scratch_enums.Position):
        pass
    def goto_x_y(self, position: scratch_enums.Coordinates):
        pass
    def glide(self, duration: int, position: scratch_enums.Coordinates):
        pass
    def point_in_direction(self, direction: int | float):
        pass
    def point_towards(self, position: scratch_enums.Position.MOUSE_POINTER | Sprite):
        pass
    def change_x_by(self, x: int | float):
        pass
    def set_x_to(self, x: int | float):
        pass
    def change_y_by(self, y: int | float):
        pass
    def set_y_to(self, y: int | float):
        pass
    def if_on_edge_bounce(self):
        pass
    def set_rotation_style(self, rotation_style: scratch_enums.RotationStyle):
        pass

    # looks
    def say_for(self, message: str, duration: int | float):
        pass
    def say(self, message: str):
        pass
    def think_for(self, message: str, duration: int | float):
        pass
    def think(self, message: str):
        pass