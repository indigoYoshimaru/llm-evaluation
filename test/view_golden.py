from typing import Text, Union, List, Dict


def read_json(file_path: Text) -> Union[List, Dict]:
    import json

    with open(file_path) as f:
        output = json.load(f)
    return output


print(read_json("dataset/20240415_114301.json"))
