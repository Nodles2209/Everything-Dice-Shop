import os
import json


def load_items():
    root = os.path.realpath(os.path.dirname(__file__))
    json_path = os.path.join(root, "json", "all_items.json")
    with open(json_path) as json_file:
        all_items = json.load(json_file)
        return all_items
