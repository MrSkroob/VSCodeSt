import scratch_project
import scratch_enums


sprite = scratch_project.Sprite("Sprite1")

def green_flag_clicked():
    sprite.say_for("Hello!", 1)
    sprite.say("Hello!")
    sprite.goto(scratch_enums.Position.MOUSE_POINTER)

sprite.green_flag_clicked(green_flag_clicked)
