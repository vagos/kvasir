from enum import Enum
from dataclasses import dataclass
from pathlib import Path

from .utils import logger

class Language(Enum):
    JS = "javascript"
    HS = "haskell"

    def __str__(self):
        return self.value.capitalize()

def detect_language(entry):
    """Detect the programming language based on the file extension."""
    if entry.endswith(".js"):
        return Language.JS
    elif entry.endswith(".hs"):
        return Language.HS
    else:
        raise ValueError(f"Unsupported file type: {entry}")

class ProgramMeta(type):
    registry = {}
    def __call__(cls, entry, *args, **kwargs):
        lang = detect_language(entry)
        subclass = cls.registry.get(lang.value, cls)
        logger.info(f"Detected language: {lang}, using subclass: {subclass.__name__} from {cls.registry}")
        return super(ProgramMeta, subclass).__call__(entry, *args, **kwargs)

@dataclass
class Program(metaclass=ProgramMeta):
    language: Language # Set by subclasses
    annotations: dict  # For plugins to store data
    entry: Path
    def __init__(self, entry):
        self.entry = Path(entry)
        self.annotations = {}
        self.code = self.load()

    def load(self) -> str:
        """Load the program code from the entry file."""
        with open(self.entry, 'r') as file:
            return file.read()

    def save(self, output):
        """Save the program code to the output file."""
        with open(output, 'w') as file:
            file.write(self.code)

    def __setitem__(self, key, value):
        self.annotations[key] = value

    def __getitem__(self, key):
        return self.annotations.get(key, None)
