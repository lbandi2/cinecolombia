import os
import json

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

def json_secret(key, attr='', json_filename='.secrets.json'):
    with open(f"{DIR_PATH}/{json_filename}", "r") as json_file:
        content = json.load(json_file)
        if attr != '':
            try:
                return content[key][attr]
            except KeyError:
                raise AttributeError(f"[ERROR] JSON attr '{attr}' in key '{key}' does not exist in '{json_filename}'")
        else:
            try:
                return content[key]
            except KeyError:
                raise KeyError(f"[ERROR] JSON key '{key}' does not exist in '{json_filename}'")
