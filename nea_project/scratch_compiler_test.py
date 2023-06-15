# testing for basic idea of adding blocks to a scratch project.
# this one is for a basic block.
import json
import zipfile
from dependencies import project_loading_utils


BLOCK_DATA = {
    "opcode": "",
    "next": None,
    "parent": None,
    "inputs": {},
    "fields": {},
    "shadow": False,
    "topLevel": True,
    "x": 0,
    "y": 0
}
PROCEDURE_DATA = {
    "opcode": "procedures_call",
    'next': '', 
    'parent': None, 
    'inputs': {
        "custom_block": [
            1,
            "" # block_id
        ]
    },
    "fields": {},
    "shadow": False,
    "x": 0,
    "y": 0
}
PROCEDURE_PROTOTYPE_DATA = {
    "opcode": "procedures_prototype",
    'next': '', 
    'parent': '', 
    'inputs': {
        "" # id
    },
    "fields": {},
    "shadow": False,
    "mutation": {
        "tagName": "mutation",
        "children": [], # this is normally empty anyway,
        "proccode": "", # procedure name
        "argumentids": "", # this is really cursed, it's an array within a string?
        "argumentdefaults": "", # same amount of curse-ness as argumentids
        "warp": False
    },
    "x": 0,
    "y": 0
}


def get_block_opcode() -> dict:
    with open("scratch_block_data.json") as f:
        json_file = json.load(f)
    return json_file


def add_block_to_project(project_json: dict, target_index: int, opcode_data: dict):
    """Adds a block to the project json"""
    target = project_json["targets"][target_index]
    target_scripts = target["blocks"]

    block_to_add = BLOCK_DATA.copy()
    block_to_add["opcode"] = opcode_data["turn_right"]
    block_to_add["inputs"] = {"DEGREES": [1, [4, "15"]]}
    


def save_data(file_name: str, data):
    """Updates the json data inside the scratch project"""
    with zipfile.ZipFile(file_name, mode="w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as f:
        json_dumped = json.dumps(data, ensure_ascii=False)
        f.writestr("project.json", data=json_dumped)
        f.testzip()


def main():
    file_name = input("File name to compile to: ")
    project_json = project_loading_utils.load_project(file_name)


if __name__ == "main":
    main()