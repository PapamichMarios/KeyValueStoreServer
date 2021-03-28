import json
from collections import defaultdict


class Trie:

    def __init__(self):
        self.root = defaultdict()

    def put(self, key: str, value: dict):
        current = self.root
        for letter in key:
            current = current.setdefault(letter, {})
        current.setdefault("_end", value)

    def delete(self, key):
        current = self.root
        for letter in key:
            current = current[letter]
        del current["_end"]

    # return a tuple of (value, object-type)
    def query(self, value: dict, subkeys: list, level: int) -> str:
        # check if first time value is a dict
        if not isinstance(value, dict):
            return ""

        for key in value.keys():

            if key == subkeys[level]:

                if level + 1 == len(subkeys):
                    return json.dumps(value[key]).replace(",", ";")

                if isinstance(value[key], dict):
                    return self.query(value=value[key], subkeys=subkeys, level=level + 1)
                else:
                    return ""

        return ""

    def get(self, key: str) -> dict:
        current = self.root
        for letter in key:
            if letter not in current:
                return {}
            current = current[letter]
        if "_end" in current:
            return current["_end"]

        return {}
