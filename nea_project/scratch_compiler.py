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
FUNCTION_NAME = r"(?<=def )(.*$)"


def contains_ignore(line: str):
    for i in IGNORE:
        if i in line:
            return True
    return False


def contains(line: str, item):
    return item in line


def get_block_data():
    with open("scratch_block_data.json") as f:
        json_file = json.load(f)
    return json_file


def load_project(file_name: str) -> json:
    with zipfile.ZipFile(file_name) as f:
        project_file = json.loads(f.read("project.json").decode("utf-8"))
    return project_file


def compile(code: list, compile_to: str):
    # load_project(compile_to)
    block_id = 0
    parent = ""
    parent_variable_name = ""
    layer = []
    compiled_result = {}
    for index in range(len(code)): # oh god i feel like im gonna commit sewerslide after this
        line = code[index]

        split = line.split(" ")
        no_whitespace = line.strip()

        if no_whitespace.find("from") != -1: continue
        if no_whitespace.find("import") != -1: continue
        if not no_whitespace: continue

        indents = len(line) - len(line.lstrip())

        if contains(line, ".Sprite("):
            if parent:
                raise scratch_exceptions.TooManySprites
            
            re_object = re.search(BETWEEN_BRACKETS, line)
            parent = re_object.group()

            parent_variable_name = line.split(" ")[0]

        if not parent: raise scratch_exceptions.MissingSpriteOrStudio

        if no_whitespace == "return":
            raise scratch_exceptions.NoReturn
        
        if contains(line, "def "): # defined a function
            function_name_re = re.search(FUNCTION_NAME, line)
            if function_name_re:
                function_name = function_name_re.group()
                compiled_result[str(block_id)] = json_data["def"]
                
                try:
                    func_index = index
                    func_line = code[func_index + 1]

                    func_indents = indents = len(line) - len(line.lstrip())
                    while func_indents != indents:
                        func_indents = func_line[func_index]
                        func_index += 1
                except IndexError:
                    pass
            else:
                raise scratch_exceptions.NoAnonymousProcedures
            
            layer.append([indents, "function"])

        elif len(layer) > 0 and indents == layer[0][0]:
            layer.pop()
        
        if contains(line, parent_variable_name + "."):
            print("scratch block found :D")
            block_name = ""
            pass

        block_id += 1

    raise NotImplementedError("If we reached here, that means code probably has no problems")
    # with zipfile.ZipFile(compile_to, "w") as f:
    #     json.dumps()


def load_python_file(file_name: str):
    with open(file_name, "r") as f:
        compile(f.readlines(), None)


if __name__ == "__main__":
    json_data = get_block_data()
    load_python_file("scratch_example.py")