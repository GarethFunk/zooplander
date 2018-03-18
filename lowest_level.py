import json


def read_globals():
    with open('globals.txt') as json_data:
        d = json.load(json_data)
        return d
