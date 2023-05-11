class TooManySprites(Exception):
    def __init__(self):
        message = "Only 1 sprite per script file"
        super().__init__(message)


class NoArgumentsAllowed(Exception):
    def __init__(self):
        message = "Scratch limitation - functions cannot have arguments"
        super().__init__(message)


class NoReturn(Exception):
    def __init__(self):
        message = "Scratch limitation - functions cannot return anything"
        super().__init__(message)


class MissingSpriteOrStudio(Exception):
    def __init__(self):
        message = "Couldn't find Sprite or Studio object"
        super().__init__(message)


class UnsuportedMethod(Exception):
    def __init__(self):
        message = "Couldn't find an equivilant Scratch block for this method"
        super().__init__(message)