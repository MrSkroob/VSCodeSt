from math import floor


def OutputTable(number: float, length: int):
    if length < 1: return # validatepyth
    length = floor(length)
    longestlen = len(str(length)) # longestlen - currentlen to get number of spaces to add
    for i in range(1, length + 1):
        currentlen = len(str(i))
        formattedmultiple = f"{i}" + " " * (longestlen - currentlen) # adds spaces in front of the multiple for formatting
        print(f"{number} x {formattedmultiple} = {number * i}")


def Interface():
    try:
        number = float(input("Which table?"))
        length = int(input("How long should it be?"))
    except ValueError:
        return
    OutputTable(number, length)
    return


Interface()