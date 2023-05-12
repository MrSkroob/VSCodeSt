class TooManySprites(Exception):
    def __init__(self):
        message = "Only 1 sprite per script file"
        super().__init__(message)


class NoReturn(Exception):
    def __init__(self):
        message = "Scratch limitation - procedures only"
        super().__init__(message)


class MissingSpriteOrStudio(Exception):
    def __init__(self):
        message = "Couldn't find Sprite or Studio object"
        super().__init__(message)


class UnsuportedMethod(Exception):
    def __init__(self):
        message = "Couldn't find an equivilant Scratch block for this method"
        super().__init__(message)


class NoAnonymousProcedures(Exception):
    def __init__(self):
        message = "Scratch limitation - procedures must have names!"
        super().__init__(message)