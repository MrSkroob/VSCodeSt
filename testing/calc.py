def calc(operation: str, *numbers):
    """Returns the result of the numbers operated on by the operation, left to right"""
    equation = ""
    last = (len(numbers) - 1)
    for i, v in enumerate(numbers):
        if i == last:
            equation += str(v)
        else:
            equation += str(v) + operation
    return eval(equation)
