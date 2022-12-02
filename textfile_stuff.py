import os

path = r"C://Users//Yacco//Documents//School"


def print_text_file(path: str):
    with open(path, "r") as f:
        for line in f:
            print(line)

def display_paths(path: str, indents=0):
    indent = "  "
    for filename in os.listdir(path):
        file = os.path.join(path, filename)
        if not os.path.isfile(file):
            print(indent * indents + f"> {filename}")
            display_paths(file, indents + 1)
        else:
            print(indent * (indents + 1) + f"| {filename}")

display_paths(path)
# print_text_file(r"C://Users//Yacco//Documents//School//CS//Work//I_stole_this//stormtrooper.txt")