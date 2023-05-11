import zipfile
import json
import re
import scratch_exceptions


IGNORE = [
    "from",
    "import"
]


# useful regexes
BETWEEN_BRACKETS = r"(?<=\()(.*?)(?=\))"
LEFT_VARIABLE_DEFINE = r"\w+\s?="
RIGHT_VARIABLE_DEFINE = r"=\s?\w+"


def contains_ignore(line: str):
    for i in IGNORE:
        if i in line:
            return True
    return False


def contains(line: str, item):
    return item in line


def load_project(file_name: str):
    with zipfile.ZipFile(file_name) as f:
        project_file = json.loads(f.read("project.json").decode("utf-8"))
    return project_file


def compile(code: list, compile_to: str):
    # load_project(compile_to)
    block_id = 0
    parent = ""
    parent_variable_name = ""
    layer = []
    for i in code: # oh god i feel like im gonna commit sewerslide after this
        split = i.split(" ")
        no_whitespace = i.strip()

        if no_whitespace.find("from") != -1: continue
        if no_whitespace.find("import") != -1: continue
        if not no_whitespace: continue

        indents = len(i) - len(i.lstrip())

        if contains(i, ".Sprite("):
            if parent:
                raise scratch_exceptions.TooManySprites
            
            re_object = re.search(BETWEEN_BRACKETS, i)
            parent = re_object.group()

            parent_variable_name = i.split(" ")[0]

        if not parent: raise scratch_exceptions.MissingSpriteOrStudio

        if no_whitespace == "return":
            raise scratch_exceptions.NoReturn
        
        if contains(i, "def "): # defined a function
            re_object = re.search(BETWEEN_BRACKETS, i)
            if re_object.group():
                raise scratch_exceptions.NoArgumentsAllowed
            
            layer.append([indents, "function"])
        elif len(layer) > 0 and indents == layer[0][0]:
            layer.pop()
        
        if contains(i, parent_variable_name + "."):
            print("scratch block found :D")
            block_name = ""
            pass

        block_id += 1

    raise NotImplementedError("If we reached here, that means code probably has no problems?")
    # with zipfile.ZipFile(compile_to, "w") as f:
    #     json.dumps()


def load_python_file(file_name: str):
    with open(file_name, "r") as f:
        compile(f.readlines(), None)


load_python_file("scratch_example.py")