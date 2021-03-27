from collections import defaultdict


class Trie:

    def __init__(self):
        self.root = defaultdict()

    def put(self, key: str, value: list):
        current = self.root
        for letter in key:
            current = current.setdefault(letter, {})
        current.setdefault("_end", value)

    def delete(self):
        return False

    def query(self):
        return False

    def get(self, key: str) -> list:
        current = self.root
        for letter in key:
            if letter not in current:
                return []
            current = current[letter]
        if "_end" in current:
            return current["_end"]

        return []
