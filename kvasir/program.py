from enum import Enum

class Language(Enum):
    JS = "javascript"
    HS = "haskell"

    def __str__(self):
        return self.value.capitalize()

class Program:
    def __init__(self, entry):
        self.entry = entry
        self.annotations = {}  # Plugins can write here

    def save(self, output):
        pass

    def __setitem__(self, key, value):
        self.annotations[key] = value

    def __getitem__(self, key):
        return self.annotations.get(key, None)

    def __repr__(self):
        return f"Program({self.entry=}, {self.annotations=})"
