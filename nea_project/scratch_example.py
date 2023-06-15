from dependencies import scratch_project, scratch_enums
# import scratch_compiler

sprite = scratch_project.Sprite("Sprite1")

def green_flag_clicked():
    sprite.say_for("Hello!", 1)
    sprite.say("Hello!")
    sprite.create_clone_of()
    sprite.go_to(scratch_enums.Position.MOUSE_POINTER)

sprite.green_flag_clicked(green_flag_clicked)
